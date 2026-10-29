# ==============================================================================
# Scene:      QuaternionRotationOverlay
# Source:     videos/_2018/quaternions.py (lines 970-1018)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuaternionRotationOverlay.py QuaternionRotationOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuaternionRotationOverlay(Scene):
    def construct(self):
        equations = VGroup(
            OldTex(
                "p", "\\rightarrow",
                "{}",
                "{}",
                "\\left(q_1",
                "p",
                "q_1^{-1}\\right)",
                "{}",
                "{}",
            ),
            OldTex(
                "p", "\\rightarrow",
                "{}",
                "\\left(q_2",
                "\\left(q_1",
                "p",
                "q_1^{-1}\\right)",
                "q_2^{-1}\\right)",
                "{}",
            ),
            OldTex(
                "p", "\\rightarrow",
                "\\left(q_3",
                "\\left(q_2",
                "\\left(q_1",
                "p",
                "q_1^{-1}\\right)",
                "q_2^{-1}\\right)",
                "q_3^{-1}\\right)",
            ),
        )
        for equation in equations:
            equation.set_color_by_tex_to_color_map({
                "1": GREEN, "2": RED, "3": BLUE,
            })
            equation.set_color_by_tex("rightarrow", WHITE)
            equation.to_corner(UL)

        equation = equations[0].copy()
        self.play(Write(equation))
        self.wait()
        for new_equation in equations[1:]:
            self.play(
                Transform(equation, new_equation)
            )
            self.wait(2)
