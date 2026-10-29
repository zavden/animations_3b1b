# ==============================================================================
# Scene:      TracePropertyAndComputation
# Source:     videos/_2021/matrix_exp.py (lines 5881-5927)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TracePropertyAndComputation.py TracePropertyAndComputation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TracePropertyAndComputation(TeacherStudentsScene):
    def construct(self):
        trace_eq = OldTex(
            "\\text{Det}\\left(e^{Mt}\\right) = e^{\\text{Tr}(M) t}",
            tex_to_color_map={
                "\\text{Det}": GREEN_D,
                "\\text{Tr}": RED_B,
            }
        )
        trace_eq.move_to(self.hold_up_spot, DOWN)

        self.play(
            self.teacher.change("raise_right_hand", trace_eq),
            FadeIn(trace_eq, 0.5 * UP),
        )
        self.play_student_changes("pondering", "confused", "pondering", look_at=trace_eq)
        self.wait(2)

        text = OldTexText("Diagonalization $\\rightarrow$ Easier computation")
        text.move_to(self.hold_up_spot, DOWN)
        text.shift_onto_screen()

        self.play(
            trace_eq.animate.shift(UP),
            FadeIn(text, 0.5 * UP),
            self.change_students("erm", "tease", "maybe"),
        )
        for pi in self.pi_creatures:  # Why?
            pi.eyes[0].refresh_bounding_box()
            pi.eyes[1].refresh_bounding_box()
        self.look_at(text)
        self.wait(3)

        topics = VGroup(trace_eq, text)

        exp_deriv = OldTex("e", "{d \\over dx}")
        exp_deriv[0].scale(2)
        exp_deriv[1].move_to(exp_deriv[0].get_corner(UR), DL)
        exp_deriv.move_to(self.hold_up_spot, DOWN)

        self.play(
            FadeIn(exp_deriv, scale=2),
            topics.animate.scale(0.5).to_corner(UL),
            self.teacher.change("tease", exp_deriv),
        )
        self.play_student_changes("confused", "sassy", "angry")
        self.wait(6)
