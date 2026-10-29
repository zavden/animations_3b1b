# ==============================================================================
# Scene:      SimplerQuadraticFormula
# Source:     videos/_2021/quick_eigen.py (lines 2649-2673)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimplerQuadraticFormula.py SimplerQuadraticFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

MEAN_COLOR = BLUE_B


PROD_COLOR = BLUE_D


class SimplerQuadraticFormula(Scene):
    def construct(self):
        # Show comparison
        form1 = OldTex(
            "{m} \\pm \\sqrt{\\,{m}^2 - {p}}",
            tex_to_color_map={"{m}": MEAN_COLOR, "{p}": PROD_COLOR},
            font_size=72
        )
        words = OldTexText("takes less to\\\\remember than")
        form2 = OldTex(
            "{-b \\pm \\sqrt{\\,b^2 - 4ac} \\over 2a}",
            tex_to_color_map={
                "a": MAROON_A,
                "b": MAROON_B,
                "c": MAROON_C,
            },
            font_size=72
        )
        group = VGroup(form1, words, form2)
        group.arrange(DOWN, buff=1.5)

        self.add(form1)
        self.play(Write(words, run_time=1))
        self.play(FadeIn(form2, DOWN))
        self.wait()
