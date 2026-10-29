# ==============================================================================
# Scene:      ShowVaryingExpFactor
# Source:     videos/_2020/covid.py (lines 1862-1878)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowVaryingExpFactor.py ShowVaryingExpFactor -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowVaryingExpFactor(Scene):
    def construct(self):
        factor = DecimalNumber(0.15)
        rect = BackgroundRectangle(factor, buff=SMALL_BUFF)
        rect.set_fill(BLACK, 1)
        arrow = Arrow(
            factor.get_right(),
            factor.get_right() + 4 * RIGHT + 0.5 * DOWN,
        )

        self.add(rect, factor, arrow)
        for value in [0.05, 0.25, 0.15]:
            self.play(
                ChangeDecimalToValue(factor, value),
                run_time=3,
            )
        self.wait()
