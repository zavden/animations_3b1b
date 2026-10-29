# ==============================================================================
# Scene:      ShowRangeOfCnFormulas
# Source:     videos/_2019/diffyq/part4/staging.py (lines 1752-1796)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowRangeOfCnFormulas.py ShowRangeOfCnFormulas -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowRangeOfCnFormulas(Scene):
    def construct(self):
        formulas = VGroup(*[
            self.get_formula(n)
            for n in [-50, None, -1, 0, 1, None, 50]
        ])
        formulas.scale(0.7)
        formulas.arrange(
            DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT
        )
        dots = formulas[1::4]
        dots.shift(MED_LARGE_BUFF * RIGHT)

        formulas.set_height(FRAME_HEIGHT - 0.5)
        formulas.to_edge(LEFT)

        self.play(LaggedStartMap(
            FadeInFrom, formulas,
            lambda m: (m, UP),
            lag_ratio=0.2,
            run_time=4,
        ))
        self.wait()

    def get_formula(self, n):
        if n is None:
            return OldTex("\\vdots")
        light_pink = interpolate_color(PINK, WHITE, 0.25)
        n_str = "{" + str(n) + "}"
        neg_n_str = "{" + str(-n) + "}"
        expression = OldTex(
            "c_" + n_str, "=",
            "\\int_0^1 f({t})",
            "e^{", neg_n_str,
            "\\cdot 2\\pi i {t}}{dt}",
            tex_to_color_map={
                "{t}": light_pink,
                "{dt}": light_pink,
                n_str: YELLOW,
                neg_n_str: YELLOW,
            }
        )
        return expression
