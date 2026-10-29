# ==============================================================================
# Scene:      Assumptions
# Source:     videos/_2021/quick_eigen.py (lines 218-265)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Assumptions.py Assumptions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Assumptions(TeacherStudentsScene):
    def construct(self):
        self.play(
            PiCreatureSays(self.teacher, OldTexText("I'm assuming you know\\\\ what eigenvalues are.")),
            self.change_students(
                "erm", "happy", "tease",
                look_at=ORIGIN,
            ),
            run_time=2,
        )
        self.play(self.students[0].change("guilty").look(LEFT))
        self.wait()

        eigen_expression = OldTex("""
            \\text{det}\\left( \\left[ \\begin{array}{cc}
                3 - \\lambda & 1 \\\\
                4 & 1 - \\lambda
            \\end{array} \\right] \\right)
        """)
        eigen_expression.move_to(self.hold_up_spot, DOWN)
        eigen_expression.to_edge(RIGHT, buff=2)
        VGroup(eigen_expression[0][7], eigen_expression[0][12]).set_color(TEAL)
        cross = Cross(eigen_expression)
        cross.set_stroke(RED, width=(2, 5, 5, 2))
        words = Text("Not this!")
        words.set_color(RED)
        words.next_to(cross, UP, MED_LARGE_BUFF)

        self.play(
            RemovePiCreatureBubble(self.teacher, target_mode="raise_right_hand"),
            FadeIn(eigen_expression, UP),
            self.students[1].change("hesitant"),
            self.students[2].change("sassy"),
        )
        self.play(
            ShowCreation(cross),
            FadeIn(words, 0.25 * UP),
            self.teacher.change("tease", cross),
            self.students[1].change("pondering", cross),
            self.students[2].change("hesitant", cross),
        )
        self.wait(3)
        fade_rect = FullScreenFadeRectangle()
        fade_rect.set_fill(BLACK, opacity=0.7)
        self.add(fade_rect, self.students[0])
        self.play(FadeIn(fade_rect))
        self.play(self.students[0].change("maybe", cross))
        self.play(Blink(self.students[0]))
