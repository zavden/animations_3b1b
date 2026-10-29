# ==============================================================================
# Scene:      DivCurlDotCross
# Source:     videos/_2018/div_curl.py (lines 3459-3474)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DivCurlDotCross.py DivCurlDotCross -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DivCurlDotCross(Scene):
    def construct(self):
        rects = VGroup(*[
            ScreenRectangle(height=2.5)
            for n in range(4)
        ])
        rects.arrange_in_grid(n_rows=2, buff=LARGE_BUFF)
        rects[2:].shift(MED_LARGE_BUFF * DOWN)
        titles = VGroup(*list(map(TexText, [
            "Divergence", "Curl",
            "Dot product", "Cross product"
        ])))
        for title, rect in zip(titles, rects):
            title.next_to(rect, UP)

        self.add(rects, titles)
