"""Builds a "clean" assets folder: a copy of the folders the scenes read in _lib/assets/ without any file
identical (by content) to one in videos/assets/, the folder Grant removed from his repo (level 3).

It serves to render as the published repo would be: with THREEB1B_ASSETS=<folder> (read by
_lib/manim_imports_ext.py), a scene that secretly depends on one of Grant's files fails instead of using it.
_lib/assets/ is not touched.

Usage:
    python _tools/make_clean_assets.py [--videos ../videos] [--out _tools/.cache/assets_limpios]"""
from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "_lib" / "assets"
# What manim_imports_ext.py passes to manim_config.directories (+ fonts)
SUBDIRS = ("PiCreature", "svg_images", "raster_images", "models", "sounds", "fonts")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--videos", type=Path, default=ROOT.parent / "videos")
    p.add_argument("--out", type=Path, default=ROOT / "_tools" / ".cache" / "assets_limpios")
    a = p.parse_args()
    grant = {digest(f) for f in (a.videos / "assets").rglob("*") if f.is_file()}
    if not grant:
        raise SystemExit(f"No encuentro archivos en {a.videos / 'assets'}")
    out = a.out.resolve()
    if out.exists():
        shutil.rmtree(out)
    copied, skipped = 0, []
    for sub in SUBDIRS:
        (out / sub).mkdir(parents=True, exist_ok=True)
        for f in sorted((ASSETS / sub).rglob("*")):
            if not f.is_file():
                continue
            rel = f.relative_to(ASSETS)
            if digest(f) in grant:
                skipped.append(str(rel))
                continue
            (out / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, out / rel)
            copied += 1
    (out / "EXCLUIDOS.txt").write_text("\n".join(skipped) + "\n")
    print(f"{out}: {copied} archivos copiados, {len(skipped)} excluidos por ser idénticos a videos/assets "
          f"(lista en EXCLUIDOS.txt)")


if __name__ == "__main__":
    main()
