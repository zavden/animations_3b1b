# ==============================================================================
# Scene:      FourierSeriesFormula
# Source:     videos/_2019/diffyq/part4/staging.py (lines 13-24)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FourierSeriesFormula.py FourierSeriesFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FourierSeriesFormula(Scene):
    def construct(self):
        formula = OldTex(
            "c_{n} = \\int_0^1 e^{-2\\pi i {n} {t}}f({t}){dt}",
            tex_to_color_map={
                "{n}": YELLOW,
                "{t}": PINK,
            }
        )

        self.play(Write(formula))
        self.wait()
