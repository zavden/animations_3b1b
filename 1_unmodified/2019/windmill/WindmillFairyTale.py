# ==============================================================================
# Scene:      WindmillFairyTale
# Source:     videos/_2019/windmill.py (lines 3716-3736)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WindmillFairyTale.py WindmillFairyTale -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WindmillFairyTale(Scene):
    def construct(self):
        paths = SVGMobject(file_name="windmill_fairytale")

        paths.set_height(FRAME_HEIGHT - 1)
        paths.set_stroke(width=0)
        paths.set_fill([GREY_B, WHITE])

        for path in paths:
            path.reverse_points()

        self.play(Write(paths[0], run_time=3))
        self.wait()
        self.play(
            LaggedStart(
                FadeIn(paths[1], RIGHT),
                FadeIn(paths[2], RIGHT),
                lag_ratio=0.2,
                run_time=3,
            )
        )
