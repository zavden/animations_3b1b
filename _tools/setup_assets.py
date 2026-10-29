"""Rebuilds locally the assets and data that the scenes need.

The published repository includes no binary asset. This script:
  1. Copies the original assets from a clone of 3b1b/videos to _lib/assets/.
  2. Generates the pi creature SVGs in the format the current code expects.
  3. Runs the generators in _lib/assets/generated/ (own placeholders and
     conversions of 3b1b assets, e.g. .ai -> .svg).
  4. Renders the few assets that are frames of scenes (requires manimgl).
  5. Copies next to each scene the data files it reads (data_manifest.json).

Usage:
    git clone https://github.com/3b1b/videos ../videos
    python _tools/setup_assets.py --videos ../videos [--skip-renders]"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "_tools"
ASSETS = ROOT / "_lib" / "assets"
GENERATED = ASSETS / "generated"

# Generators in order: some read assets left by the previous step
GENERATORS = [
    # Own Π character (3b1b's pi creatures = level 3); first: others read PiCreature/happy.svg
    "pi_creature/install_pi.py",
    "2026/cross_entropy/make_cross_entropy_placeholders.py",
    "2026/print_gallery/make_print_gallery_assets.py",
    "2026/monthly_mindbenders/make_ladybug_svg.py",
    "2026/hairy_ball/make_s3_viking_placeholder.py",
    "outside_videos/talent/make_talent_svgs.py",
    "2025/grover/make_grover_svgs.py",
    "2025/cosmic_distance/make_cosmic_distance_assets.py",
    "2025/cosmic_distance/make_cosmic_distance_images.py",
    "2024/inscribed_rect/make_inscribed_rect_svgs.py",
    "2024/inscribed_rect/make_inscribed_rect_images.py",
    "2024/transformers/make_transformers_data.py",
    "2024/transformers/make_chm_assets.py",
    "2024/transformers/make_supplements_assets.py",
    "2024/transformers/make_generation_assets.py",
    "2024/transformers/make_generation_data.py",
    "2024/transformers/make_embedding_images.py",
    "2024/transformers/make_attention_images.py",
    "2024/transformers/make_mlp_images.py",
    "2024/transformers/make_ml_basics_data.py",
    "2024/holograms/make_holograms_assets.py",
    "2023/optics_puzzles/make_optics_puzzles_assets.py",
    "2023/gauss_int/make_gauss_int_placeholders.py",
    "2023/SoME3/make_some3_assets.py",
    "2023/clt/make_clt_assets.py",
    "2023/convolutions2/make_convolutions2_assets.py",
    "2023/moser_reboot/make_moser_reboot_assets.py",
    "2023/standup_maths/make_standup_maths_assets.py",
    "2022/piano/make_piano_assets.py",
    "2022/wordle/make_wordle_assets.py",
    "2022/wordle/make_wordle_wordlists.py",
    "2022/wordle/make_wordle_data.py",
    "2021/quick_eigen/make_quick_eigen_assets.py",
    "2021/shadows/make_shadows_assets.py",
    "outside_videos/short_links/make_short_links_assets.py",
    "outside_videos/for_site/make_for_site_assets.py",
    "2021/matrix_exp/make_matrix_exp_assets.py",
    "2021/newton_fractal/make_newton_fractal_assets.py",
    "2021/siggraph/make_siggraph_assets.py",
    "2021/some1/make_some1_assets.py",
    "2022/convolutions/make_convolutions_images.py",
    "2022/galois/make_galois_assets.py",
    "2022/infinity/make_infinity_assets.py",
    "2022/puzzles/make_puzzles_assets.py",
    "2022/some2/make_some2_assets.py",
    "2022/visual_proofs/make_lies_images.py",
    "2019/spirals/make_primes.py",
    "2019/windmill/make_windmill_data.py",
    "fonts/get_fonts.py",
    "misc_placeholders.py",
    # Level 3 replacements: they go last because they overwrite names from the assets copy
    "replacements/visual/make_visual_svgs.py",
    "replacements/visual/make_visual_rasters.py",
    "replacements/visual/make_video_cards.py",
    # SVG icons and 2020 logos that came from Grant's assets/ (R5); they overwrite the copies from videos/assets
    "replacements/visual/make_visual_svgs_2020.py",
    "replacements/photos/make_replacement_photos.py",
    "replacements/sounds/make_replacement_sounds.py",
    # Derivatives (reversed and slower) of clack.wav and slow_clack.wav: after those two are replaced
    "2025/colliding_blocks_v2/make_clack_sounds.py",
    # Real photos and textures from free sources (download with cache and license verification); the second
    # copies each one to its duplicates (raster_images <-> generated) and redoes the dark Moon and Mars textures
    "replacements/downloads/make_downloaded_assets.py",
    "replacements/downloads/propagate_downloads.py",
    # 2020 images that came from Grant's assets/: free downloads and recreations by code (Codex)
    "replacements/assets2020/make_assets_2020.py",
    # Images supplied by the user (Codex); overrides markers and photos above
    "replacements/codex/install_codex.py",
]

# Assets that are a frame of a scene: (script, scene, destination)
FRAME_RENDERS = [
    ("2026/2025_P6/make_RandomGrid_png_scene.py", "RandomGridThumbnailTest",
     ASSETS / "raster_images" / "RandomGrid.png"),
    ("2025/laplace/make_DynamicExpIntuitionStill.py", "DynamicExpIntuitionStill",
     GENERATED / "2025/laplace/DynamicExpIntuitionStill.png"),
    ("2025/laplace/make_LaplaceFormulaStill.py", "LaplaceFormulaStill",
     GENERATED / "2025/laplace/LaplaceFormulaStill.png"),
]


def step(msg):
    print(f"\n==> {msg}", flush=True)


def copy_original_assets(videos: Path):
    src = videos / "assets"
    if not src.is_dir():
        raise SystemExit(f"No encuentro {src}: ¿es un clon de 3b1b/videos?")
    for item in src.iterdir():
        dst = ASSETS / item.name
        if item.is_dir():
            shutil.copytree(item, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dst)
    # (the own TauCreatures_* are installed by pi_creature/install_pi.py directly into svg_images)
    for sub in ("models", "raster_images", "svg_images", "sounds"):
        (ASSETS / sub).mkdir(parents=True, exist_ok=True)


def run_generators(env):
    for rel in GENERATORS:
        script = GENERATED / rel
        print(f"   {rel}", flush=True)
        subprocess.run([sys.executable, str(script)], cwd=script.parent, env=env, check=True,
                       stdout=subprocess.DEVNULL)


def render_frames(env):
    for rel, scene, dest in FRAME_RENDERS:
        script = GENERATED / rel
        out = ROOT / "renders" / "_setup"
        print(f"   {scene} -> {dest.relative_to(ROOT)}", flush=True)
        proc = subprocess.run(
            [sys.executable, str(TOOLS / "render.py"), str(script), scene, "--out", str(out)],
            env=env, capture_output=True, text=True,
        )
        res = json.loads(proc.stdout.strip().splitlines()[-1])
        if res["status"] != "ok":
            print(f"   ! falló el render de {scene}; ver {res.get('log')}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if res.get("image"):
            shutil.copy2(res["image"], dest)
        else:  # it was not static: the last frame of the video is taken
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.1", "-i", res["video"],
                            "-frames:v", "1", str(dest)], check=True)


def copy_data_files(videos: Path):
    manifest = json.loads((TOOLS / "data_manifest.json").read_text())
    missing = 0
    for entry in manifest:
        base = videos if entry["from"] == "videos" else ROOT
        src = base / entry["src"]
        dst = ROOT / entry["scene_dir"] / entry["dst"]
        if not src.exists():
            missing += 1
            print(f"   ! falta {src}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
    print(f"   {len(manifest) - missing} copiados, {missing} faltantes")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--videos", type=Path, required=True, help="clon local de github.com/3b1b/videos")
    p.add_argument("--skip-renders", action="store_true", help="no renderizar los assets que son fotogramas")
    a = p.parse_args()
    videos = a.videos.resolve()
    env = {**os.environ, "THREEB1B_VIDEOS": str(videos), "PYTHONPATH": str(ROOT / "_lib")}

    step("Copiando assets originales de 3b1b/videos")
    copy_original_assets(videos)
    step("Generando SVG de pi creatures")
    subprocess.run([sys.executable, str(TOOLS / "make_pi_creature_svgs.py")], check=True, stdout=subprocess.DEVNULL)
    step("Ejecutando generadores de assets")
    run_generators(env)
    if not a.skip_renders:
        step("Renderizando assets que son fotogramas de escenas")
        render_frames(env)
    step("Copiando archivos de datos junto a las escenas")
    copy_data_files(videos)
    print("\nListo.")


if __name__ == "__main__":
    main()
