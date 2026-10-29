# ==============================================================================
# Scene:      MoreGeneralSystem
# Source:     videos/_2021/matrix_exp.py (lines 1932-1951)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoreGeneralSystem.py MoreGeneralSystem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoreGeneralSystem(Scene):
    def construct(self):
        kw = {
            "tex_to_color_map": {
                "x": RED,
                "y": GREEN,
                "z": BLUE,
                "{t}": GREY_B,
            }
        }
        equations = VGroup(
            OldTex("{dx \\over d{t} } = a\\cdot x({t}) + b\\cdot y({t}) + c\\cdot z({t})", **kw),
            OldTex("{dy \\over d{t} } = d\\cdot x({t}) + e\\cdot y({t}) + f\\cdot z({t})", **kw),
            OldTex("{dz \\over d{t} } = g\\cdot x({t}) + h\\cdot y({t}) + i\\cdot z({t})", **kw),
        )
        equations.arrange(DOWN, buff=LARGE_BUFF)

        self.add(equations)
        self.play(LaggedStartMap(FadeIn, equations, shift=UP, lag_ratio=0.5, run_time=3))
        self.wait()
