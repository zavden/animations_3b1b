# ==============================================================================
# Scene:      SmoothHilbertZoom
# Source:     videos/_2017/fractal_dimension.py (lines 2425-2453)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SmoothHilbertZoom.py SmoothHilbertZoom -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SmoothHilbertZoom(Scene):
    def construct(self):
        hilbert = HilbertCurve(
            order = 7,
            color = MAROON_B,
            monochromatic = True
        )
        hilbert.make_smooth()
        self.add(hilbert)

        two_d_title = OldTexText("2D at a distance...")
        one_d_title = OldTexText("1D up close")
        for title in two_d_title, one_d_title:
            title.to_edge(UP)

        self.add(two_d_title)
        self.wait()
        self.play(
            ApplyMethod(
                hilbert.scale, 100,
                hilbert.point_from_proportion(0.3),
            ),
            Transform(
                two_d_title, one_d_title,
                rate_func = squish_rate_func(smooth)
            ),
            run_time = 3
        )
        self.wait()
