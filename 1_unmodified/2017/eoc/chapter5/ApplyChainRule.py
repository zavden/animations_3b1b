# ==============================================================================
# Scene:      ApplyChainRule
# Source:     videos/_2017/eoc/chapter5.py (lines 1238-1282)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ApplyChainRule.py ApplyChainRule -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ApplyChainRule(TeacherStudentsScene):
    def construct(self):
        deriv_equation = OldTex(
            "{d(", "e^", "{3", "t}", ")", "\\over", "dt}",
            "=", "3", "e^", "{3", "t}",
        )
        deriv_equation.next_to(self.teacher, UP+LEFT)
        deriv_equation.shift(UP)
        deriv_equation.set_color_by_tex("3", BLUE)
        deriv = VGroup(*deriv_equation[:7])
        exponent = VGroup(*deriv_equation[-2:])
        circle = Circle(color = YELLOW)
        circle.replace(exponent, stretch = True)
        circle.scale(1.5)

        self.teacher_says("Think of the \\\\ chain rule")
        self.play_student_changes(*["pondering"]*3)
        self.play(
            Write(deriv),
            RemovePiCreatureBubble(
                self.teacher,
                target_mode = "raise_right_hand"
            ),
        )
        self.wait(2)
        self.play(*[
            Transform(
                *deriv_equation.get_parts_by_tex(
                    tex, substring = False
                ).copy()[:2],
                path_arc = -np.pi,
                run_time = 2
            )
            for tex in ("e^", "{3", "t}")
        ] + [
            Write(deriv_equation.get_part_by_tex("="))
        ])
        self.play(self.teacher.change_mode, "happy")
        self.wait()
        self.play(ShowCreation(circle))
        self.play(Transform(
            *deriv_equation.get_parts_by_tex("3").copy()[-1:-3:-1]
        ))
        self.play(FadeOut(circle))
        self.wait(3)
