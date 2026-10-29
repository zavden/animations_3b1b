"""Renders ONE scene with manimgl respecting the global render queue.

Rules (do not change without talking to the user):
- Always `-w`; never `-p` or `-f`.
- 720p at 15 fps by default (`--hd` / `--fps` only if quality is truly needed).
- At most 2 renders at a time on the whole machine: each render takes one of
  the 2 slots (lock files in _tools/.locks). If both are busy, it waits.

Usage:
    python render.py <file.py> <Scene> --out <folder> [--timeout 900] [--hd | --low] [--fps 30]

Prints a JSON with: status (ok|error|timeout), seconds, video, thumb, duration, error, log."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
LOCK_DIR = TOOLS / ".locks"
TIKTOKEN_CACHE = TOOLS / ".cache" / "tiktoken"
WORK_DIR = TOOLS / ".work"
N_SLOTS = 3  # 3 renders at a time (2026-10-28: the user lowered it from 4 after a GPU hang, ring gfx timeout, that took down Xorg and the session)
# Memory cap per render (cgroup via systemd-run). With 14 GB of RAM and 2 renders at once, a scene
# that exceeds it dies on its own instead of triggering the system's global OOM killer.
MEMORY_MAX = "5G"
# The manimgl from the same environment that runs this script
MANIMGL = Path(sys.executable).with_name("manimgl")
if not MANIMGL.exists():
    # Outside the venv (e.g. with the system python): the manimgl from the user's venv
    MANIMGL = Path(shutil.which("manimgl") or TOOLS.parents[1] / "manimgl/venv/bin/manimgl")


def acquire_slot():
    LOCK_DIR.mkdir(exist_ok=True)
    while True:
        for i in range(N_SLOTS):
            f = open(LOCK_DIR / f"slot{i}.lock", "w")
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return i, f
            except BlockingIOError:
                f.close()
        time.sleep(2)


def probe_duration(video: Path) -> float | None:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(video)],
            capture_output=True, text=True, timeout=30,
        )
        return float(out.stdout.strip())
    except Exception:
        return None


def make_thumb(video: Path, duration: float | None) -> Path | None:
    thumb = video.with_suffix(".jpg")
    t = max(0.0, (duration or 0) * 0.6)
    proc = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video),
         "-frames:v", "1", "-vf", "scale=426:-2", str(thumb)],
        capture_output=True, timeout=60,
    )
    return thumb if proc.returncode == 0 and thumb.exists() else None


def extract_error(log: str) -> str:
    lines = [l for l in log.splitlines() if l.strip()]
    tb_start = None
    for i, l in enumerate(lines):
        if l.startswith("Traceback (most recent call last)"):
            tb_start = i
    if tb_start is not None:
        # Without Python 3.13's ~~~^^^ marker lines, which take up half the traceback
        tail = [l for l in lines[tb_start:] if l.strip(" ~^")]
        # The cause is the last line "XxxError: ..."; whatever comes after is later output
        # (warnings, progress bars) and must not displace it
        ends = [i for i, l in enumerate(tail) if re.match(r"[A-Za-z_][\w.]*(Error|Exception|Interrupt|Exit)\b", l)]
        if ends:
            tail = tail[:ends[-1] + 1]
        # Deepest location inside the scene file + the final line of the error
        return "\n".join(tail[-12:])
    return "\n".join(lines[-12:])


def run_manimgl(cmd: list[str], cwd: Path, log_path: Path, timeout: int, append=False) -> str:
    """Runs manimgl with the log in log_path. Returns "ok", "error" or "timeout"."""
    with open(log_path, "a" if append else "w") as log_file:
        log_file.write("$ " + " ".join(cmd) + "\n")
        log_file.flush()
        proc = subprocess.Popen(
            cmd, cwd=cwd, stdout=log_file, stderr=subprocess.STDOUT,
            start_new_session=True,
            # No Hugging Face downloads: no scene downloads model weights (GPT-2 etc.)
            env={**os.environ, "PYTHONUNBUFFERED": "1",
                 "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1",
                 # tiktoken keeps its vocabulary in /tmp, which is erased on reboot
                 "TIKTOKEN_CACHE_DIR": str(TIKTOKEN_CACHE)},
        )
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            return "timeout"
    log = log_path.read_text(errors="replace")
    if proc.returncode < 0 or proc.returncode == 128 + signal.SIGKILL:
        # Killed by SIGKILL (cgroup memory cap): leaves no traceback
        with open(log_path, "a") as log_file:
            log_file.write(f"\n[render.py] manimgl fue terminado con SIGKILL: casi seguro superó "
                           f"el tope de memoria de {MEMORY_MAX}.\n")
        return "error"
    if proc.returncode != 0 or "Traceback (most recent call last)" in log:
        return "error"
    return "ok"


def render(file: Path, scene: str, out_dir: Path, timeout: int, hd: bool, fps: int | None, low: bool = False,
           res: str | None = None):
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / f"{scene}.log"
    video = out_dir / f"{scene}.mp4"
    image = out_dir / f"{scene}.png"
    for old in (video, image):
        if old.exists():
            old.unlink()

    slot, lock = acquire_slot()
    # It runs from the scene's folder (some read data with relative paths), but each slot uses its
    # own LaTeX cache: manimgl always compiles in <latex_cache>/working.tex and two renders in
    # parallel would overwrite each other.
    slot_dir = WORK_DIR / f"slot{slot}"
    slot_dir.mkdir(parents=True, exist_ok=True)
    slot_config = slot_dir / "config.yml"
    slot_config.write_text(
        f"directories:\n  subdirs:\n    latex_cache: \"{slot_dir / 'latex_cache'}\"\n"
    )
    # The memory cap needs systemd (Linux); on other systems it renders without it
    memory_cap = [
        "systemd-run", "--user", "--scope", "--quiet",
        "-p", f"MemoryMax={MEMORY_MAX}", "-p", "MemorySwapMax=0",
    ] if shutil.which("systemd-run") else []
    cmd = [
        *memory_cap,
        str(MANIMGL), str(file), scene, "-w",
        *(["-r", res] if res else ["--hd"] if hd else ["-l"] if low else ["-m"]),
        "--fps", str(fps or (30 if hd else 15)),
        "--video_dir", str(out_dir),
        "--file_name", scene,
        "--config_file", str(slot_config),
    ]
    cwd = file.parent
    start = time.time()
    duration = None
    is_static = False
    try:
        status = run_manimgl(cmd, cwd, log_path, timeout)
        if status == "ok" and not video.exists():
            status = "error"
        if status == "ok":
            duration = probe_duration(video)
            # Static scenes (only self.add, no play/wait) produce an empty mp4: in that case the
            # last frame is saved as an image with -s.
            if duration is None or duration < 0.05:
                is_static = True
                video.unlink(missing_ok=True)
                status = run_manimgl(cmd + ["-s"], cwd, log_path, timeout, append=True)
                if status == "ok" and not image.exists():
                    status = "error"
    finally:
        fcntl.flock(lock, fcntl.LOCK_UN)
        lock.close()
    seconds = round(time.time() - start, 1)

    log = log_path.read_text(errors="replace")
    result = {"status": status, "seconds": seconds, "log": str(log_path)}
    if status == "ok" and is_static:
        thumb = out_dir / f"{scene}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(image), "-vf", "scale=426:-2", str(thumb)],
            capture_output=True, timeout=60,
        )
        result.update(image=str(image), static=True, thumb=str(thumb) if thumb.exists() else None)
    elif status == "ok":
        thumb = make_thumb(video, duration)
        result.update(video=str(video), duration=duration, thumb=str(thumb) if thumb else None)
        if duration < 0.2:
            result["warning"] = "video casi vacío"
    elif status == "timeout":
        result["error"] = f"Superó el límite de {timeout}s\n" + extract_error(log)
    else:
        result["error"] = extract_error(log) or "manimgl terminó sin producir video"
    # manimgl leaves <Scene>_temp.mp4 half-written when it fails
    temp = out_dir / f"{scene}_temp.mp4"
    if temp.exists():
        temp.unlink()
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("file", type=Path)
    p.add_argument("scene")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--timeout", type=int, default=900)
    p.add_argument("--hd", action="store_true")
    p.add_argument("--fps", type=int)
    p.add_argument("--low", action="store_true", help="480p, solo para comprobar que una escena corre")
    p.add_argument("--res", help="resolución exacta, p. ej. 640x360 (tiene prioridad sobre --hd/--low)")
    a = p.parse_args()
    res = render(a.file.resolve(), a.scene, a.out.resolve(), a.timeout, a.hd, a.fps, a.low, a.res)
    print(json.dumps(res, ensure_ascii=False))
    sys.exit(0 if res["status"] == "ok" else 1)


if __name__ == "__main__":
    main()
