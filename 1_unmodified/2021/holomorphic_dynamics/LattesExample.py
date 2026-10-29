# ==============================================================================
# Scene:      LattesExample
# Source:     videos/_2021/holomorphic_dynamics.py (lines 3365-3409)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LattesExample.py LattesExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LattesExample(TeacherStudentsScene):
    def construct(self):
        example = VGroup(
            OldTexText("Lattè's example: "),
            OldTex(r"L(z)=\frac{\left(z^{2}+1\right)^{2}}{4 z\left(z^{2}-1\right)}"),
        )
        example.arrange(RIGHT)
        example[0].shift(SMALL_BUFF * DOWN)
        example.move_to(self.hold_up_spot, DOWN)
        example.set_x(0)

        j_fact = OldTexText("Julia set of $L(z)$ is all of $\\mathds{C}$")
        j_fact.move_to(example)
        subwords = OldTexText("(and the point at $\\infty$)", font_size=36)
        subwords.set_fill(GREY_A)
        subwords.next_to(j_fact, DOWN)

        self.play(
            self.teacher.change("raise_right_hand", 3 * UR),
            self.change_students(
                "pondering", "happy", "tease",
                look_at=3 * UR
            )
        )
        self.wait(3)
        self.play(
            self.teacher.change("sassy", example),
            Write(example)
        )
        self.play_student_changes(
            "pondering", "pondering", "pondering",
            look_at=example,
        )

        self.play(
            example.animate.to_edge(UP),
            FadeIn(j_fact),
            self.change_students(
                "erm", "erm", "erm",
                look_at=j_fact,
            ),
            self.teacher.change("raise_right_hand", j_fact)
        )
        self.play(FadeIn(subwords))
        self.wait(3)
