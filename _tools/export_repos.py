"""Builds /home/.../learning/repos/ for publishing (2017-2026 and outside_videos; 2016 and earlier are left out). The repo
names (the GitHub ones) are in repo_names.py:

  manimgl_3b1b/     clone of the fork (fixes branch, with its history, no remote) + DIFF.md with the changes since fafa083
  assets_3b1b/      the clean folder (_tools/.cache/assets_limpios, no files of Grant's) + the scripts that generate it
  animations_3b1b/  the scenes by category, _lib/, _tools/ and the web pages in html/ (index.html and learning.html)
  renders_3b1b/     the videos for Google Drive (dropped into animations_3b1b/html/renders_3b1b/)

It also leaves inside animations_3b1b/ a copy of renders_3b1b/ (in html/) and of assets_3b1b/, both in its
.gitignore, to try the web pages and the scenes without downloading anything. The copies use reflink: on btrfs they
take no space. It only runs `git init` (no commits or remotes). It can be run again: it keeps the .git folders and
rebuilds the rest. At the end it translates everything into English (traduccion/apply.py) unless --no-translate is given.

Usage: python export_repos.py [--only manimgl,assets,renders,animations] [--target ../../repos]"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.argv, _argv = sys.argv[:1], sys.argv  # pipeline.py reads sys.argv when it is imported
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pipeline as P
import repo_names as N
from export_repo import scrub, check_no_local_paths, TEXT_SUFFIXES
sys.argv = _argv

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
LEARNING = ROOT.parent
FORK = LEARNING / "manimgl"
BASE_COMMIT = "fafa083"
CLEAN_ASSETS = TOOLS / ".cache" / "assets_limpios"
EXPORT_FILES = TOOLS / "export_files"
# Top-level folders (inside each category and renders/) that are published
SCOPE_DIRS = ("2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "outside_videos")
SCOPE_SOURCES = tuple(f"_{y}" for y in SCOPE_DIRS[:-1]) + ("outside_videos",)
TOOL_FILES = [
    "extract.py", "render.py", "pipeline.py", "placeholder.py", "make_pi_creature_svgs.py",
    "setup_assets.py", "find_default_arg_updaters.py", "make_clean_assets.py", "export_repo.py", "export_repos.py",
    "repo_names.py", "index_template.html", "order.txt", "aprendizaje/make_preview.py", "aprendizaje/preview_template.html",
]
# Level 2 data (downloaded from their source) and level 4 data (regenerated): they are in the local copy but not in git
DATA_IGNORE = [
    "pattern_matrix.npy", "glove-wiki-gigaword-50*", "tale_of_two_cities.txt", "PiCreaturePointCloud.csv",
    "nbaShots*.csv", "galactic_data.csv", "simulation_results/", "best_entropies.json",
    "best_double_entropies.json", "best_scores_with_entropy_method.json", "salet_with_brute_force_guess_map.json",
    "ent_score_pairs.json",
]


def run(*cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def reflink_copy(src: Path, dst: Path):
    """Copies a whole folder with cp --reflink=auto (instant on btrfs), replacing dst"""
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    run("cp", "-a", "--reflink=auto", str(src), str(dst))


def clean_dir(target: Path, keep=(".git",)):
    target.mkdir(parents=True, exist_ok=True)
    for item in target.iterdir():
        if item.name in keep:
            continue
        shutil.rmtree(item) if item.is_dir() else item.unlink()


def git_init(repo: Path):
    if not (repo / ".git").exists():
        run("git", "init", "-q", "-b", "main", str(repo))


def copy_text(src: Path, dst: Path):
    """Copies removing the local paths from text files; the others (or those that are not UTF-8) as they are"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix in TEXT_SUFFIXES:
        try:
            dst.write_text(scrub(src.read_text(encoding="utf-8")), encoding="utf-8")
            shutil.copystat(src, dst)
            return
        except UnicodeDecodeError:
            pass
    shutil.copy2(src, dst)


def copy_tree_scrubbed(src: Path, dst: Path, skip=lambda p: False):
    for f in sorted(src.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts and f.name != ".DS_Store" and not skip(f):
            copy_text(f, dst / f.relative_to(src))


# ---------------------------------------------------------------- manimgl

def export_manimgl(target: Path):
    repo = target / N.MANIMGL
    if not (repo / ".git").exists():
        run("git", "clone", "-q", "--branch", "fixes", str(FORK), str(repo))
        run("git", "branch", "-q", "master", "origin/master", cwd=repo)
        run("git", "remote", "remove", "origin", cwd=repo)
    git = lambda *a: subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True, check=True).stdout
    commits = git("log", "--reverse", "--format=%h|%ad|%s", "--date=short", f"{BASE_COMMIT}..fixes").splitlines()
    lines = [
        "# Changes from upstream commit `fafa083`",
        "",
        "This fork is based on [3b1b/manim](https://github.com/3b1b/manim) at commit",
        "[`fafa083`](https://github.com/3b1b/manim/commit/fafa083a4fb274bba9cabde0b6e2f50ba6da0622)",
        "(\"Add VideoMobject and Sprite (#2521)\", 2026-09-09). The `fixes` branch adds the commits below.",
        "[`FORK_CHANGES.md`](FORK_CHANGES.md) explains each fix (symptom, cause and test); this file lists",
        "every commit and the full code diff.",
        "",
        f"## Commits ({len(commits)})",
        "",
        "| # | Commit | Date | Title |",
        "|---|---|---|---|",
    ]
    lines += [f"| {i} | `{h}` | {d} | {s} |" for i, (h, d, s) in
              enumerate((c.split("|", 2) for c in commits), 1)]
    lines += ["", "## Files changed", "", "```", git("diff", "--stat=100", BASE_COMMIT, "fixes").rstrip(), "```",
              "", "## Full diff of `manimlib/`", "", "```diff",
              git("diff", BASE_COMMIT, "fixes", "--", "manimlib").rstrip(), "```", ""]
    (repo / "DIFF.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"manimgl: {len(commits)} commits sobre {BASE_COMMIT}, DIFF.md escrito")


# ---------------------------------------------------------------- assets

def export_assets(target: Path):
    repo = target / N.ASSETS
    if not CLEAN_ASSETS.is_dir():
        run(sys.executable, str(TOOLS / "make_clean_assets.py"))
    clean_dir(repo)
    for item in sorted(CLEAN_ASSETS.iterdir()):
        if item.is_dir():
            reflink_copy(item, repo / item.name)
    for ds in repo.rglob(".DS_Store"):
        ds.unlink()
    # The scripts that generated the placeholders and their sources (author, license and URL of each download)
    gen = ROOT / "_lib" / "assets" / "generated"
    # (also the 2019 ones: their assets go in the clean folder)
    copy_tree_scrubbed(gen, repo / "generated",
                       skip=lambda f: not (f.suffix == ".py" or f.name.endswith("_sources.json")))
    copy_text(EXPORT_FILES / "assets" / "README.md", repo / "README.md")
    copy_text(EXPORT_FILES / "LICENSE", repo / "LICENSE")
    copy_text(ROOT / "ATTRIBUTIONS.md", repo / "ATTRIBUTIONS.md")
    git_init(repo)
    n = sum(1 for f in repo.rglob("*") if f.is_file() and ".git" not in f.parts)
    print(f"assets: {n} archivos")
    if leaks := check_no_local_paths(repo):
        print("ATENCIÓN, rutas locales en:", *leaks[:20], sep="\n  ")


# ---------------------------------------------------------------- renders

def export_renders(target: Path):
    out = target / N.RENDERS
    clean_dir(out, keep=())
    for name in SCOPE_DIRS:
        if (ROOT / "renders" / name).is_dir():
            reflink_copy(ROOT / "renders" / name, out / name)
    for log in out.rglob("*.log"):  # the logs have local paths and are of no use to whoever downloads the videos
        log.unlink()
    copy_text(EXPORT_FILES / "renders" / "README.md", out / "README.md")
    n = sum(1 for f in out.rglob("*.mp4"))
    print(f"renders: {n} videos")


# ---------------------------------------------------------------- animations

def in_scope(entry: dict) -> bool:
    return entry["source"].startswith(SCOPE_SOURCES)


def export_animations(target: Path):
    repo = target / N.ANIMATIONS
    clean_dir(repo)
    for cat_dir in P.CATEGORY_DIRS.values():
        for name in SCOPE_DIRS:
            if (ROOT / cat_dir / name).is_dir():
                copy_tree_scrubbed(ROOT / cat_dir / name, repo / cat_dir / name)
    lib = ROOT / "_lib"
    for f in lib.glob("*.py"):
        copy_text(f, repo / "_lib" / f.name)
    for sub in ("custom", "once_useful_constructs"):
        copy_tree_scrubbed(lib / sub, repo / "_lib" / sub)
    copy_tree_scrubbed(lib / "data", repo / "_lib" / "data")
    for name in TOOL_FILES:
        copy_text(TOOLS / name, repo / "_tools" / name)
    copy_text(EXPORT_FILES / "LICENSE-tools", repo / "_tools" / "LICENSE")

    # Web: the index with the filtered catalog and the learning page, with the links to the code in ../
    catalog = [e for e in json.loads((ROOT / "catalog.json").read_text()) if in_scope(e)]
    (repo / "catalog.json").write_text(scrub(json.dumps(catalog, indent=1, ensure_ascii=False)), encoding="utf-8")
    code_root = ('const CODE_ROOT = "";', 'const CODE_ROOT = "../";')
    data = json.dumps(catalog, ensure_ascii=False).replace("</", "<\\/")
    index = (TOOLS / "index_template.html").read_text().replace("/*__CATALOG__*/[]", data)
    learning = (ROOT / "learning.html").read_text()
    pages = [("index.html", index), ("learning.html", learning)]
    if (ROOT / "skipped.html").exists():  # list of skipped scenes (make_ignoradas.py)
        pages.append(("skipped.html", (ROOT / "skipped.html").read_text()))
    for name, html in pages:
        assert html.count(code_root[0]) == 1, name
        (repo / "html").mkdir(exist_ok=True)
        (repo / "html" / name).write_text(scrub(html.replace(*code_root)), encoding="utf-8")

    for name in ("README.md", "LICENSE", "requirements.txt", "pyproject.toml", ".gitignore"):
        copy_text(EXPORT_FILES / "animations" / name if (EXPORT_FILES / "animations" / name).exists()
                  else EXPORT_FILES / name, repo / name)
    with open(repo / ".gitignore", "a", encoding="utf-8") as f:
        f.write("\n# Datos de nivel 2 (se descargan) y 4 (se regeneran): ver ATTRIBUTIONS.md\n")
        f.write("".join(f"{p}\n" for p in DATA_IGNORE))
    copy_text(ROOT / "ATTRIBUTIONS.md", repo / "ATTRIBUTIONS.md")

    # Local copies (in .gitignore): the videos for the web and the assets repo for the scenes
    reflink_copy(target / N.RENDERS, repo / "html" / N.RENDERS)
    (repo / N.ASSETS).mkdir()
    for item in sorted((target / N.ASSETS).iterdir()):
        if item.name != ".git":
            reflink_copy(item, repo / N.ASSETS / item.name) if item.is_dir() else shutil.copy2(item, repo / N.ASSETS)
    git_init(repo)
    n_scenes = sum(1 for e in catalog if e.get("file"))
    print(f"animations: {n_scenes} escenas, {len(catalog)} entradas en el catálogo")
    leaks = [p for p in check_no_local_paths(repo) if p.parts[0] != N.ASSETS and p.parts[:2] != ("html", N.RENDERS)]
    if leaks:
        print("ATENCIÓN, rutas locales en:", *leaks[:20], sep="\n  ")


def publish_web_paths(target: Path):
    """Last step: in the web pages and the catalog, the videos live in html/<renders>/ (repo_names.py), not in html/renders/"""
    repo = target / N.ANIMATIONS
    for f in [*(repo / "html").glob("*.html"), repo / "catalog.json", repo / "_tools" / "index_template.html",
              repo / "_tools" / "aprendizaje" / "preview_template.html"]:
        text = f.read_text(encoding="utf-8")
        new = text.replace('"renders/', f'"{N.RENDERS}/').replace("html/renders/", f"html/{N.RENDERS}/")
        if new != text:
            f.write_text(new, encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--target", type=Path, default=LEARNING / "repos")
    p.add_argument("--only", default="manimgl,assets,renders,animations")
    p.add_argument("--no-translate", action="store_true", help="skip the English translation step (traduccion/apply.py)")
    a = p.parse_args()
    target = a.target.resolve()
    steps = {"manimgl": export_manimgl, "assets": export_assets, "renders": export_renders,
             "animations": export_animations}
    for name in a.only.split(","):
        steps[name](target)
    if not a.no_translate:
        # Last step: English translation of what was exported (maps in _tools/traduccion/, see its apply.py)
        sys.path.insert(0, str(TOOLS / "traduccion"))
        import apply as repo_translation
        done = [n for n in a.only.split(",") if n in ("animations", "assets", "renders")]
        # assets goes first: it also translates the local copy that export_animations leaves in animations/assets/
        for n in sorted(done, key=["assets", "animations", "renders"].index):
            print(f"translation ({n}):", repo_translation.STEPS[n](target))
    if "animations" in a.only.split(","):
        publish_web_paths(target)


if __name__ == "__main__":
    main()
