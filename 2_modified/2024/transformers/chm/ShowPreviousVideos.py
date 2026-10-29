# ==============================================================================
# Scene:      ShowPreviousVideos
# Source:     videos/_2024/transformers/chm.py (lines 2107-2153)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowPreviousVideos.py ShowPreviousVideos -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The 7 YouTube thumbnails (downloaded at run time) are replaced with local color cards with the video title (yt_card_<id>.png)
#
# Placeholder assets (not Grant's originals):
#   - raster_images/yt_card_<id>.png of the Deep Learning series (_lib/assets/generated/replacements/visual/make_video_cards.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ShowPreviousVideos(InteractiveScene):
    def construct(self):
        # Backdrop
        background = FullScreenRectangle()
        self.add(background)

        line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        line.set_stroke(WHITE, 2)

        series_name = Text("Deep Learning Series", font_size=68)
        series_name.to_edge(UP, buff=0.35)
        self.add(series_name)

        # Show thumbnails
        thumbnails = Group(
            Group(
                Rectangle(16, 9).set_height(1).set_stroke(WHITE, 2),
                # CHANGE: the YouTube thumbnail was downloaded at run time; now it is a local color card with the title (raster_images/yt_card_<id>.png, make_video_cards.py)
                ImageMobject(f"yt_card_{slug}", height=1)
            )
            for slug in [
                "aircAruvnKk",
                "IHZwWFHWa-w",
                "Ilg3gGewQ5U",
                "tIeHLnjs5U8",
                "wjZofJX0v4M",
                "eMlx5fFNoYc",
                "9-Jl0dxWQs8",
            ]
        )

        thumbnails.arrange_in_grid(n_cols=4, buff=0.2)
        thumbnails.set_width(FRAME_WIDTH - 1)
        thumbnails.next_to(series_name, DOWN, buff=1.0)
        thumbnails[-3:].set_x(0)

        self.play(LaggedStartMap(FadeIn, thumbnails, shift=0.3 * UP, lag_ratio=0.35, run_time=4))
        self.wait()

        # Rearrange
        left_x = -FRAME_WIDTH / 4
        self.play(
            series_name.animate.set_x(left_x),
            thumbnails.animate.arrange_in_grid(n_cols=2, buff=0.25).set_height(6).set_x(left_x).to_edge(DOWN),
            ShowCreation(line, time_span=(1, 2)),
            run_time=2,
        )
        self.wait()
