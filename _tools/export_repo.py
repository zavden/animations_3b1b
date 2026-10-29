"""Builds a publishable copy of converted/ in another folder: only own code and text.

It includes:
  - The final scenes (categories 1, 2 and 4) and the sibling .py files they read.
  - _lib/: manim_imports_ext.py, custom/, once_useful_constructs/, data/ (own placeholders)
    and the generator scripts of _lib/assets/generated/ (without their results).
  - _tools/ (MIT license), index.html and catalog.json.
  - data_manifest.json: which data files go next to each scene and where they come from,
    so that _tools/setup_assets.py can rebuild them.
It does not include: binary assets (neither 3b1b's nor own), renders, _work/ nor _meta/.

Usage: python export_repo.py [--target ../../3b1b-videos-manimgl]
If the destination is already a git repo, .git is kept and the rest is replaced."""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
LEARNING = ROOT.parent

CATEGORY_DIRS = ["1_unmodified", "2_modified", "3_not_rendering", "4_interactive"]
TOOL_FILES = [
    "extract.py", "render.py", "pipeline.py", "placeholder.py", "make_pi_creature_svgs.py",
    "setup_assets.py", "find_default_arg_updaters.py", "export_repo.py",
    "index_template.html", "order.txt",
]
TEXT_SUFFIXES = {".py", ".md", ".txt", ".json", ".html", ".glsl", ".toml", ".yml", ""}
# Local paths that must not appear in a public repo
SCRUB = [
    (str(ROOT) + "/", ""),
    (str(LEARNING / "videos") + "/", "videos/"),
    (str(LEARNING / "manimgl"), "manimgl"),
    (str(Path.home()), "~"),
]


def scrub(text: str) -> str:
    for old, new in SCRUB:
        text = text.replace(old, new)
    return text


def copy_text(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix in TEXT_SUFFIXES:
        dst.write_text(scrub(src.read_text(encoding="utf-8")), encoding="utf-8")
    else:
        shutil.copy2(src, dst)


def clean_target(target: Path):
    if target.exists():
        for item in target.iterdir():
            if item.name == ".git":
                continue
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    target.mkdir(parents=True, exist_ok=True)


def export_scenes(target: Path, catalog: list[dict]) -> list[dict]:
    """Copies scenes and sibling .py files; returns the manifest of non-.py data."""
    by_key = {(e["scene"], e["source"]): e for e in catalog if e.get("file")}
    manifest = []
    for meta_path in sorted((ROOT / "_meta").rglob("*.json")):
        meta = json.loads(meta_path.read_text())
        entry = by_key.get((meta["scene"], meta["source"]))
        if entry is None:
            continue
        scene_file = ROOT / entry["file"]
        copy_text(scene_file, target / entry["file"])
        scene_dir = scene_file.parent.relative_to(ROOT)
        src_dir = Path(meta["source"]).parent
        for item in meta.get("data_files", []):
            if isinstance(item, str):
                src, dst, origin = src_dir / item, item, "videos"
            else:
                abs_src = Path(item["src"])
                dst = item["dst"]
                if abs_src.is_relative_to(ROOT):
                    src, origin = abs_src.relative_to(ROOT), "repo"
                else:
                    src, origin = abs_src.relative_to(LEARNING / "videos"), "videos"
            if Path(dst).suffix == ".py" and origin == "videos":
                # Sibling code (e.g. a module loaded with importlib): published as code
                copy_text(LEARNING / "videos" / src, target / scene_dir / dst)
                continue
            manifest.append({"scene_dir": str(scene_dir), "from": origin, "src": str(src), "dst": dst})
    return manifest


def export_lib(target: Path):
    lib, out = ROOT / "_lib", target / "_lib"
    for name in ("manim_imports_ext.py", "legacy_vector_field.py"):
        copy_text(lib / name, out / name)
    for sub in ("custom", "once_useful_constructs"):
        for f in (lib / sub).rglob("*"):
            if f.is_file() and "__pycache__" not in f.parts:
                copy_text(f, out / f.relative_to(lib))
    # Only the own top-level placeholders; the per-year subfolders (e.g. data/2024/) are generated
    # by setup_assets.py (some bring downloads: GloVe, Project Gutenberg)
    for f in (lib / "data").iterdir():
        if f.is_file():
            copy_text(f, out / "data" / f.name)
    for f in (lib / "assets" / "generated").rglob("*.py"):
        copy_text(f, out / f.relative_to(lib))


def export_tools(target: Path, manifest: list[dict]):
    for name in TOOL_FILES:
        copy_text(TOOLS / name, target / "_tools" / name)
    (target / "_tools" / "data_manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n"
    )


def export_index(target: Path):
    for name in ("index.html", "catalog.json"):
        copy_text(ROOT / name, target / name)


def check_no_local_paths(target: Path):
    leaks = []
    for f in target.rglob("*"):
        if f.is_file() and ".git" not in f.parts and f.suffix in TEXT_SUFFIXES:
            text = f.read_text(encoding="utf-8", errors="replace")
            if re.search(r"/home/[a-z]+/|/Users/(?!grant)[a-z]+/", text):
                leaks.append(f.relative_to(target))
    return leaks


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", type=Path, default=LEARNING / "3b1b-videos-manimgl")
    a = p.parse_args()
    target = a.target.resolve()
    catalog = json.loads((ROOT / "catalog.json").read_text())

    clean_target(target)
    manifest = export_scenes(target, catalog)
    export_lib(target)
    export_tools(target, manifest)
    export_index(target)
    for name in ("README.md", "LICENSE", ".gitignore", "requirements.txt", "pyproject.toml"):
        src = TOOLS / "export_files" / name
        if src.exists():
            copy_text(src, target / name)
    shutil.copy2(TOOLS / "export_files" / "LICENSE-tools", target / "_tools" / "LICENSE")

    n_scenes = sum(1 for e in catalog if e.get("file"))
    print(f"{target}: {n_scenes} escenas, {len(manifest)} archivos de datos en el manifiesto")
    leaks = check_no_local_paths(target)
    if leaks:
        print("ATENCIÓN, rutas locales en:", *leaks[:20], sep="\n  ")


if __name__ == "__main__":
    main()
