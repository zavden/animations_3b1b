"""Pipeline for converting scenes from 3b1b/videos to converted/.

Flow:
  1. extract   Extracts each scene from the source files to _work/ (working copy)
               and saves the original version intact as <Scene>.orig.py.
  2. render    Renders scenes from _work/ (via render.py, max. 4 at a time).
               If the working copy is identical to the original and renders -> category 1;
               if it was modified and renders -> category 2.
  3. finalize  Copies each scene to its category folder with an explanatory
               header and regenerates index.html and catalog.json.
  sync-data    Copies again to _work/ the data_files {"src", "dst"} (generated assets) that changed
               since the extract; the original repo's data do not change and are not touched. It goes before the final re-render.

The source of truth are the JSONs in _meta/<source path>/<Scene>.json.
Fields that are edited by hand (or by the agents):
  changes        list of changes made to the working copy (category 2)
  gave_up        true if it could not be made to render (category 3)
  reason         why it does not render (category 3)
  interactive    "ejecutable" | "no_ejecutable" (category 4)
  interaction    instructions to play with the scene (category 4)
  data_files     data files to copy next to the scene: paths relative
                 to the source file's folder, or {"src": absolute_path, "dst": relative}
  assets_created placeholder assets created for this scene (makes it category 2)
  packages       packages installed in the venv for this scene
  notes          free notes
  timeout        timeout seconds for this scene if it is slow (render saves it if
                 it finished with a --timeout greater than the default)

Usage:
  python pipeline.py extract <source.py> [...] [--force]
  python pipeline.py render  [--src <source.py>] [--scene X] [--status pending,error] [--force]
      batches: [--prefix _2024] [--list scenes.txt] [--exclude-list others.txt] [--out-root folder]
             [--res 640x360] [--fps 10] [--no-meta] [--log batch.log]   (live log + batch.jsonl)
  python pipeline.py finalize
  python pipeline.py status  [--src <source.py>]
  python pipeline.py sync-data [--src <source.py>] [--dry]"""
from __future__ import annotations

import argparse
import collections
import difflib
import filecmp
import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
# Clone of 3b1b/videos (by default, next to this folder)
VIDEOS = Path(os.environ.get("THREEB1B_VIDEOS", ROOT.parent / "videos")).resolve()
WORK = ROOT / "_work"
META = ROOT / "_meta"
RENDERS = ROOT / "renders"
PYTHON = sys.executable
DEFAULT_TIMEOUT = 900

CATEGORY_DIRS = {
    "1": "1_unmodified",
    "2": "2_modified",
    "3": "3_not_rendering",
    "4a": "4_interactive/runnable",
    "4b": "4_interactive/not_runnable",
}
CATEGORY_LABELS = {
    "1": "1 · Renderiza sin modificaciones",
    "2": "2 · Renderiza con modificaciones",
    "3": "3 · No renderiza",
    "4a": "4 · Interactiva (ejecutable)",
    "4b": "4 · Interactiva (no ejecutable)",
    "pending": "Pendiente de renderizar",
    "error": "Falló el render, pendiente de revisar",
    "diferida": "Diferida: diálogo de pi creatures, se renderiza al final del proyecto",
    "base": "Clase base (no es una escena final)",
}


# ---------------------------------------------------------------- paths

def rel_source(src: Path) -> Path:
    """_2026/cross_entropy/entropy.py"""
    if not src.is_absolute() and not src.exists():
        # Given as in the meta (relative to videos/), from any folder
        src = VIDEOS / src
    return src.resolve().relative_to(VIDEOS)


def display_dir(src_rel: Path) -> Path:
    """2026/cross_entropy/entropy  (without the year's underscore or the .py)"""
    parts = list(src_rel.with_suffix("").parts)
    parts[0] = parts[0].lstrip("_")
    return Path(*parts)


def meta_path(src_rel: Path, scene: str) -> Path:
    return META / src_rel.with_suffix("") / f"{scene}.json"


def work_path(src_rel: Path, scene: str) -> Path:
    return WORK / src_rel.with_suffix("") / f"{scene}.py"


def file_hash(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def load_meta(path: Path) -> dict:
    return json.loads(path.read_text())


def save_meta(path: Path, meta: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")


def all_metas(src_filter: list[Path] | None = None):
    for p in sorted(META.rglob("*.json")):
        meta = load_meta(p)
        if src_filter and meta["source"] not in {str(rel_source(s)) for s in src_filter}:
            continue
        yield p, meta


def category(meta: dict) -> str:
    if meta.get("base"):
        return "base"
    if meta.get("interactive") == "ejecutable":
        return "4a"
    if meta.get("interactive") == "no_ejecutable":
        return "4b"
    if meta.get("gave_up"):
        return "3"
    r = meta.get("render") or {}
    if r.get("status") == "ok":
        # Invented assets (placeholder images) also count as a modification
        modified = r.get("hash") != meta["orig_hash"] or meta.get("assets_created")
        return "2" if modified else "1"
    if meta.get("diferida"):
        return "diferida"
    if r:
        return "error"
    return "pending"


# ---------------------------------------------------------------- extract

def run_extract(cmd: list[str]) -> dict:
    proc = subprocess.run([PYTHON, str(TOOLS / "extract.py"), *cmd], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-2000:])
    return json.loads(proc.stdout)


def copy_data_files(meta: dict, dest_dir: Path):
    src_dir = (VIDEOS / meta["source"]).parent
    for item in meta.get("data_files", []):
        if isinstance(item, str):
            src, dst = src_dir / item, dest_dir / item
        else:
            src, dst = Path(item["src"]), dest_dir / item["dst"]
        if not src.exists():
            print(f"  ! falta el archivo de datos {src}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)


def cmd_extract(sources: list[Path], force: bool):
    for src in sources:
        src_rel = rel_source(src)
        listing = run_extract(["list", str(src)])
        print(f"{src_rel}: {len(listing['scenes'])} escenas")
        for s in listing["scenes"]:
            scene = s["scene"]
            mp = meta_path(src_rel, scene)
            if mp.exists() and not force:
                continue
            wp = work_path(src_rel, scene)
            orig = wp.with_suffix(".orig.py")
            info = run_extract(["one", str(src), scene, str(orig)])
            shutil.copy2(orig, wp)
            meta = {
                "scene": scene,
                "source": str(src_rel),
                "source_lines": s["lines"],
                "flags": s["flags"],
                "inlined_modules": info["inlined_modules"],
                "redirected_imports": info["redirected_imports"],
                "unresolved_imports": info["unresolved_imports"],
                "orig_hash": file_hash(orig),
            }
            if "sin_construct" in s["flags"]:
                meta["base"] = True
            if mp.exists():
                old = load_meta(mp)
                for key in ("changes", "assets_created", "gave_up", "reason", "interactive", "interaction",
                            "data_files", "packages", "notes"):
                    if key in old:
                        meta[key] = old[key]
            save_meta(mp, meta)


# ---------------------------------------------------------------- render

def render_one(mp: Path, meta: dict, timeout: int, opts: dict | None = None) -> dict:
    """opts (batches): out_root (output folder instead of renders/), res ("640x360"), fps and no_meta
    (do not save the result in the meta: a test batch must not change categories)."""
    opts = opts or {}
    # Re-read: an agent may have added data_files or timeout since the batch started
    meta = load_meta(mp)
    src_rel = Path(meta["source"])
    wp = work_path(src_rel, meta["scene"])
    copy_data_files(meta, wp.parent)
    out_dir = Path(opts.get("out_root") or RENDERS) / display_dir(src_rel)
    # Slow scenes remember in the meta the timeout with which they did finish
    timeout = max(timeout, meta.get("timeout", 0))
    extra = [*(["--res", opts["res"]] if opts.get("res") else []), *(["--fps", str(opts["fps"])] if opts.get("fps") else [])]
    proc = subprocess.run(
        [PYTHON, str(TOOLS / "render.py"), str(wp), meta["scene"],
         "--out", str(out_dir), "--timeout", str(timeout), *extra],
        capture_output=True, text=True,
    )
    try:
        res = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception:
        res = {"status": "error", "error": (proc.stdout + proc.stderr)[-2000:]}
    # The hash is taken when finished, not when queued: render.py waits its turn, sometimes several
    # minutes, and manimgl reads the working copy only when it starts, so a change made while
    # waiting goes into the render and the category has to see it
    res["hash"] = file_hash(wp)
    res["at"] = time.strftime("%Y-%m-%d %H:%M")
    if opts.get("no_meta"):
        return {**meta, "render": res}
    # Re-read: an agent may have edited other fields in the meantime
    meta = load_meta(mp)
    meta["render"] = res
    if res["status"] == "ok" and timeout > DEFAULT_TIMEOUT:
        meta["timeout"] = timeout
    save_meta(mp, meta)
    return meta


def read_scene_list(path: Path | None) -> dict[str, float | None] | None:
    """File with one scene per line, "source::Scene" (e.g. "_2024/transformers/mlp.py::Intro"), optionally
    followed by a tab and the estimated seconds (used by the log's remaining time). It keeps the file's order."""
    if path is None:
        return None
    out = {}
    for l in path.read_text().splitlines():
        if l.strip() and not l.startswith("#"):
            key, _, est = l.strip().partition("\t")
            out[key.strip()] = float(est) if est.strip() else None
    return out


def cmd_render(sources, scenes, statuses, force, timeout, workers, prefixes=(), only=None, exclude=None,
               opts=None, log_path: Path | None = None):
    jobs = []
    for mp, meta in all_metas(sources):
        if scenes and meta["scene"] not in scenes:
            continue
        if prefixes and not meta["source"].startswith(tuple(prefixes)):
            continue
        key = f"{meta['source']}::{meta['scene']}"
        if only is not None and key not in only:
            continue
        if exclude is not None and key in exclude:
            continue
        cat = category(meta)
        if cat == "base":
            continue
        # Deferred ones (pi dialogues, see marcar_diferidas.py) are only rendered when requested with --status diferida
        if cat == "diferida" and cat not in statuses:
            continue
        if statuses and cat not in statuses:
            continue
        if not force:
            # --force only skips this "already rendered with this code" check
            r = meta.get("render") or {}
            if r.get("status") == "ok" and r.get("hash") == file_hash(work_path(Path(meta["source"]), meta["scene"])):
                continue
        jobs.append((mp, meta, cat))
    if sources:
        # Respect the order in which the sources were passed (newest first)
        order = {str(rel_source(s)): i for i, s in enumerate(sources)}
        jobs.sort(key=lambda j: (order.get(j[1]["source"], 1e9), j[1]["source_lines"][0]))
    elif only:
        # --list: in file order
        index = {k: i for i, k in enumerate(only)}
        jobs.sort(key=lambda j: index[f"{j[1]['source']}::{j[1]['scene']}"])
    total = len(jobs)
    # Remaining time: with the estimated seconds from --list (if all are present) instead of the average, which
    # with a batch ordered from short to long falls far short
    est = {f"{j[1]['source']}::{j[1]['scene']}": (only or {}).get(f"{j[1]['source']}::{j[1]['scene']}")
           for j in jobs}
    use_est = bool(est) and all(v is not None for v in est.values())
    est_done = 0.0
    print(f"{total} escenas para renderizar")

    # Live progress log (one line per finished scene) + full results in <log>.jsonl
    lock = threading.Lock()
    counts = collections.Counter()
    start = time.time()

    def log(line: str):
        if log_path is None:
            return
        with open(log_path, "a") as f:
            f.write(line + "\n")

    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log(f"=== Lote iniciado {time.strftime('%Y-%m-%d %H:%M:%S')}: {total} escenas, {workers} en paralelo, "
            f"opciones {opts or {}}, timeout {timeout}s ===")

    def job(args):
        nonlocal est_done
        mp, meta, cat = args
        meta = render_one(mp, meta, timeout, opts)
        r = meta["render"]
        line = f"[{cat:>8}] {meta['source']}::{meta['scene']} ({r.get('seconds')}s)"
        err = ""
        if r["status"] != "ok":
            err = ((r.get("error") or "").strip().splitlines() or [""])[-1][:200]
            line += "\n          " + err
        print(line, flush=True)
        with lock:
            counts[r["status"]] += 1
            done = sum(counts.values())
            elapsed = time.time() - start
            if use_est:
                est_done += est[f"{meta['source']}::{meta['scene']}"]
                eta = elapsed * (sum(est.values()) - est_done) / max(est_done, 1e-9)
            else:
                eta = elapsed / done * (total - done)
            log(f"{time.strftime('%H:%M:%S')} [{done}/{total}] {r['status'].upper():7} [{cat:>8}] "
                f"{meta['source']}::{meta['scene']} ({r.get('seconds')}s) | ok={counts['ok']} "
                f"error={counts['error']} timeout={counts['timeout']} | quedan ~{eta / 3600:.1f} h"
                + (f"\n          {err}" if err else ""))
            if log_path is not None:
                with open(log_path.with_suffix(".jsonl"), "a") as f:
                    f.write(json.dumps({"key": f"{meta['source']}::{meta['scene']}", "categoria": cat,
                                        **{k: r.get(k) for k in ("status", "seconds", "error", "log", "video",
                                                                 "image", "duration", "warning")}},
                                       ensure_ascii=False) + "\n")

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(job, jobs))
    log(f"=== Lote terminado {time.strftime('%Y-%m-%d %H:%M:%S')}: {dict(counts)} en "
        f"{(time.time() - start) / 3600:.1f} h ===")


# ---------------------------------------------------------------- finalize

def header(meta: dict, cat: str) -> str:
    scene = meta["scene"]
    a, b = meta["source_lines"]
    lines = [
        "=" * 78,
        f"Escena:     {scene}",
        f"Origen:     videos/{meta['source']} (líneas {a}-{b})",
        f"Categoría:  {CATEGORY_LABELS[cat]}",
    ]
    if meta.get("inlined_modules"):
        lines.append("Incluye código copiado de: " + ", ".join(meta["inlined_modules"]))
    lines += [
        "",
        "Ejecutar desde esta carpeta:",
        f"    manimgl {scene}.py {scene} -w -m --fps 15",
    ]
    if cat.startswith("4"):
        lines.append(f"    manimgl {scene}.py {scene}        # ventana interactiva")
    if meta.get("interaction"):
        lines += ["", "Cómo interactuar:"] + [f"  {l}" for l in meta["interaction"].splitlines()]
    if meta.get("changes"):
        lines += ["", "Cambios respecto al original (busca '# CAMBIO' o '# CHANGE' en el código):"]
        lines += [f"  - {c}" for c in meta["changes"]]
    if meta.get("assets_created"):
        lines += ["", "Assets de relleno (no son los originales de Grant):"]
        lines += [f"  - {a}" for a in meta["assets_created"]]
    if cat == "3":
        lines += ["", "Por qué no renderiza:"] + [f"  {l}" for l in (meta.get("reason") or "?").splitlines()]
    if meta.get("packages"):
        lines += ["", "Paquetes extra instalados en el venv: " + ", ".join(meta["packages"])]
    if meta.get("notes"):
        lines += ["", "Notas:"] + [f"  {l}" for l in meta["notes"].splitlines()]
    lines.append("=" * 78)
    return "".join(f"# {l}".rstrip() + "\n" for l in lines) + "\n"


def cmd_finalize():
    for d in CATEGORY_DIRS.values():
        target = ROOT / d
        if target.exists():
            shutil.rmtree(target)
    catalog = []
    for mp, meta in all_metas():
        cat = category(meta)
        src_rel = Path(meta["source"])
        wp = work_path(src_rel, meta["scene"])
        entry = {
            "scene": meta["scene"],
            "source": meta["source"],
            "lines": meta["source_lines"],
            "year": src_rel.parts[0].lstrip("_"),
            "video": src_rel.parts[1] if len(src_rel.parts) > 2 else src_rel.stem,
            "module": src_rel.stem,
            "category": cat,
            "flags": meta.get("flags", []),
        }
        for key in ("changes", "assets_created", "reason", "interaction", "notes", "packages", "inlined_modules"):
            if meta.get(key):
                entry[key] = meta[key]
        r = meta.get("render") or {}
        if r.get("status") == "ok":
            # Only what is on disk is linked (e.g. PascalColored was left without a published video)
            media = Path(r["image"] if r.get("static") else r["video"])
            if media.exists():
                entry["image_file" if r.get("static") else "video_file"] = str(media.relative_to(ROOT))
            if r.get("thumb") and Path(r["thumb"]).exists():
                entry["thumb"] = str(Path(r["thumb"]).relative_to(ROOT))
            entry["duration"] = r.get("duration")
            entry["render_seconds"] = r.get("seconds")
        elif r.get("error"):
            entry["error"] = r["error"][-1500:]
        if cat in CATEGORY_DIRS:
            dest_dir = ROOT / CATEGORY_DIRS[cat] / display_dir(src_rel)
            dest = dest_dir / f"{meta['scene']}.py"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest.write_text(header(meta, cat) + wp.read_text(), encoding="utf-8")
            copy_data_files(meta, dest_dir)
            entry["file"] = str(dest.relative_to(ROOT))
            orig = wp.with_suffix(".orig.py")
            if cat != "1" and orig.exists() and file_hash(orig) != file_hash(wp):
                entry["diff"] = "".join(difflib.unified_diff(
                    orig.read_text().splitlines(keepends=True),
                    wp.read_text().splitlines(keepends=True),
                    "original", "convertido", n=2,
                ))[:20000]
        catalog.append(entry)

    # Index order: newest files first (according to order.txt), then by line
    order_file = TOOLS / "order.txt"
    ranks = {}
    if order_file.exists():
        for i, line in enumerate(order_file.read_text().splitlines()):
            ranks[line.split("|", 1)[1]] = i
    catalog.sort(key=lambda e: (ranks.get(e["source"], 1e9), e["lines"][0]))

    (ROOT / "catalog.json").write_text(json.dumps(catalog, indent=1, ensure_ascii=False))
    template = (TOOLS / "index_template.html").read_text()
    data = json.dumps(catalog, ensure_ascii=False).replace("</", "<\\/")
    (ROOT / "index.html").write_text(template.replace("/*__CATALOG__*/[]", data), encoding="utf-8")
    counts = {}
    for e in catalog:
        counts[e["category"]] = counts.get(e["category"], 0) + 1
    print("finalize:", counts)


def cmd_sync_data(sources, dry: bool):
    changed = 0
    for mp, meta in all_metas(sources):
        dest_dir = work_path(Path(meta["source"]), meta["scene"]).parent
        for item in meta.get("data_files", []):
            if isinstance(item, str):
                continue
            src, dst = Path(item["src"]), dest_dir / item["dst"]
            pairs = ([(f, dst / f.relative_to(src)) for f in src.rglob("*") if f.is_file()] if src.is_dir()
                     else [(src, dst)] if src.is_file() else [])
            for s, d in pairs:
                if d.exists() and filecmp.cmp(s, d, shallow=False):
                    continue
                changed += 1
                print(f"{'(dry) ' if dry else ''}{s.relative_to(ROOT)} -> {d.relative_to(ROOT)}")
                if not dry:
                    d.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(s, d)
    print(f"{changed} archivos {'por actualizar' if dry else 'actualizados'}")


def cmd_status(sources):
    counts, by_src = {}, {}
    for mp, meta in all_metas(sources):
        cat = category(meta)
        counts[cat] = counts.get(cat, 0) + 1
        by_src.setdefault(meta["source"], {}).setdefault(cat, 0)
        by_src[meta["source"]][cat] += 1
    for src, c in by_src.items():
        print(f"{src:60s} {c}")
    print("TOTAL", counts)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["extract", "render", "finalize", "status", "sync-data"])
    p.add_argument("sources", nargs="*", type=Path)
    p.add_argument("--src", action="append", type=Path, default=[])
    p.add_argument("--scene", action="append", default=[])
    p.add_argument("--status", default="")
    p.add_argument("--force", action="store_true")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--dry", action="store_true")
    # Batches (render): selection by source prefix or list of scenes, separate output and quality, live log
    p.add_argument("--prefix", action="append", default=[], help="solo fuentes que empiezan así (p. ej. _2024)")
    p.add_argument("--list", type=Path, help="solo las escenas de este archivo, en ese orden (fuente::Escena por "
                                             "línea, opcional: tab + segundos estimados)")
    p.add_argument("--exclude-list", type=Path, help="saltar las escenas de este archivo")
    p.add_argument("--out-root", type=Path, help="carpeta de salida en lugar de renders/")
    p.add_argument("--res", help="resolución exacta, p. ej. 640x360")
    p.add_argument("--fps", type=int)
    p.add_argument("--no-meta", action="store_true", help="no guardar resultados en los metas (lote de prueba)")
    p.add_argument("--log", type=Path, help="log de progreso en vivo (+ resultados en <log>.jsonl)")
    a = p.parse_args()
    sources = a.sources + a.src
    if a.cmd == "extract":
        cmd_extract(sources, a.force)
    elif a.cmd == "render":
        statuses = [s for s in a.status.split(",") if s]
        opts = {"out_root": a.out_root, "res": a.res, "fps": a.fps, "no_meta": a.no_meta}
        cmd_render(sources or None, a.scene, statuses, a.force, a.timeout, min(a.workers, 3), a.prefix,
                   read_scene_list(a.list), read_scene_list(a.exclude_list), opts, a.log)
    elif a.cmd == "finalize":
        cmd_finalize()
    elif a.cmd == "status":
        cmd_status(sources or None)
    elif a.cmd == "sync-data":
        cmd_sync_data(sources or None, a.dry)


if __name__ == "__main__":
    main()
