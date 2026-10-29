# 3b1b/videos on ManimGL 1.7.2

Scenes from the public repository of 3Blue1Brown ([3b1b/videos](https://github.com/3b1b/videos)), split into
**one file per scene** and adapted to work with ManimGL 1.7.2. Each file carries only the code its scene needs,
including the helpers copied from other modules of the repo, so it can be run on its own.

It covers the videos from **2017 to 2026** and `outside_videos`. It is not affiliated with 3Blue1Brown nor endorsed by them.

| Category | Scenes | Folder |
|---|---|---|
| Renders unmodified | 3381 | `1_unmodified/` |
| Renders with modifications | 1744 | `2_modified/` |
| Does not render (broken or test code in the original, or animated outside manim) | 140 | `3_not_rendering/` |
| Interactive (to play with in manimgl's window) | 29 | `4_interactive/runnable/` |

Inside each category: `<year>/<video>/<original file>/<Scene>.py`. The header of each file says which file and
lines of the original it comes from, how to run it and what was changed; each change in the code is marked with
`# CHANGE`.

## The three repositories

| Repository | What it has |
|---|---|
| [`manimgl_3b1b`](https://github.com/zavden/manimgl_3b1b) | The ManimGL fork with the fixes these scenes need (`FORK_CHANGES.md`, `DIFF.md`) |
| `animations_3b1b` (this one) | The scenes, `_lib/` (shared code), `_tools/` (conversion tools) and the web pages in `html/` |
| [`assets_3b1b`](https://github.com/zavden/assets_3b1b) | Images, SVGs, sounds, models and fonts that the scenes read, with their licenses |

The rendered videos (720p, 15 fps) are not on GitHub: they are downloaded from Google Drive ([link](https://drive.google.com/drive/folders/1BCGrsZvolya2Jwur21eW9Irj0JhkhujV?usp=sharing)).

## Installation

```bash
git clone https://github.com/zavden/manimgl_3b1b
pip install -e manimgl_3b1b                      # ManimGL with the fixes; needs LaTeX, dvisvgm and ffmpeg
git clone https://github.com/zavden/animations_3b1b
cd animations_3b1b
git clone https://github.com/zavden/assets_3b1b  # inside animations_3b1b/ (or next to it, in ../assets_3b1b)
pip install -r requirements.txt
pip install -e .                            # makes manim_imports_ext importable from any folder
```

`_lib/manim_imports_ext.py` uses the folder in the `THREEB1B_ASSETS` variable if you define it; otherwise it looks
for the assets in `animations_3b1b/assets_3b1b/` and then in `../assets_3b1b`.

## Running a scene

From the scene's folder (some read data through relative paths):

```bash
cd 1_unmodified/2026/cross_entropy/entropy
manimgl SpaceOfCodewords.py SpaceOfCodewords -w -m --fps 15   # to video, in ./videos/
manimgl SpaceOfCodewords.py SpaceOfCodewords                  # interactive window
```

## The web pages

`html/index.html` is the index of all the scenes, with filters by year, video and category, and the detail of each
one (command to run it, changes and diff against the original). `html/learning.html` groups the scenes by their
value for learning ManimGL, in tabs. `html/skipped.html` lists the scenes that have no render (animated outside manim,
with ZoomedScene, pi creature dialogues set aside…), the reason for each one and whether, in theory, they could be rendered with ManimCE.
All three open directly in the browser, without a server.

To see the videos, download the `renders_3b1b/` folder from [Google Drive](https://drive.google.com/drive/folders/1BCGrsZvolya2Jwur21eW9Irj0JhkhujV?usp=sharing) and put it in `html/renders_3b1b/`.

## Data that does not come in the repo

Some large data files are not in git (the list is at the end of `.gitignore`):

- **They are downloaded from their official source:** GloVe (PDDL) and the text of *A Tale of Two Cities* (Project Gutenberg).
  tiktoken downloads its vocabulary the first time it is used.
- **They are regenerated with a script:** the pattern matrix and the Wordle simulations, and some synthetic data of
  more than 10 MB.

The scripts that produce them are in `generated/` of the `assets_3b1b` repo. The scenes that use them fail until
the file is in place.

## Attribution and licenses

- **Original work:** [3b1b/videos](https://github.com/3b1b/videos) by Grant Sanderson / 3Blue1Brown, under
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
- **This repository is an adaptation** and is distributed under the same license (see `LICENSE`): you can
  share and modify it giving credit, for non-commercial purposes and under the same license.
- **Exception:** the tools in `_tools/` are new code and are under the MIT license (`_tools/LICENSE`).
- The attributions of third-party assets and data are in `ATTRIBUTIONS.md`.

| Path | License |
|---|---|
| `1_unmodified/`, `2_modified/`, `3_not_rendering/`, `4_interactive/`, `_lib/`, `html/`, `catalog.json` | CC BY-NC-SA 4.0 |
| `_tools/` | MIT |

## Differences from Grant's environment

`_lib/manim_imports_ext.py` replaces the one in the original repo and:

- points the asset directories to the assets repo instead of Grant's Dropbox;
- replicates the essentials of his `custom_config.yml` (black background, CMU Serif font) and registers the fonts in
  `assets_3b1b/fonts/`;
- looks up assets ignoring case (Grant uses macOS) and accepts `Path` paths;
- restores the updater rule from before manimgl's PR #2481: an updater receives `dt` only if it has a parameter
  named `dt`;
- accepts APIs that manimgl changed and that the 2020-2024 code uses (`set_stroke(background=)`, `FillArrow`, the
  pre-2022 `CONFIG` dicts, numpy aliases removed in numpy 2, among others);
- adapts the 2017, 2018, 2019 and 2020 code, written for ManimCairo or for an early manimgl version: `_lib/cairo_compat.py` and
  `_lib/legacy_2020.py` provide what those versions had and the current one lacks (`TexMobject`/`TextMobject`, `ThreeDScene`
  with `set_camera_orientation`, `color_using_background_image`, the `x_min`/`x_max` parameters of `Axes`, among others) and
  only act on the code of those years.

## Limitations

- The assets that Grant did not publish (copyrighted photos, logos, the original pi creatures) were replaced by
  original or freely licensed material. The header of each scene says which placeholders it uses.
- The scenes that depended on language models or private data use plausible synthetic data (among them those of `nn`, from 2017, which use a synthetic MNIST because the real one is not in the repo).
- Ten very slow scenes from 2021-2026 are published as 360p video, and three from 2018 and 2019 (`FourierOfBritain`,
  `FourierOfBritainZoomedIn` and `HangingWeightsScene`) as 480p video at 10 fps. `PascalColored` (more than an hour of render) and
  `_2021/some1_winners.py::Introduction` (fails with the fork's current version) have no video.
- Of 2017 and 2018, the pi creature dialogue scenes and those that use `ZoomedScene` (ManimCE) are not included (yet), and three scenes that
  are too heavy for this version (`PondScene` in `basel` and `basel2`, and `TinierAndTinerRectangles`) were set aside.
- `_tools/` contains the tools with which the conversion was done; `pipeline.py` needs the working metadata,
  which is not published.
