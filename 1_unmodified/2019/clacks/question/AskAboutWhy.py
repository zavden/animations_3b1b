# ==============================================================================
# Scene:      AskAboutWhy
# Source:     videos/_2019/clacks/question.py (lines 1395-1426)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutWhy.py AskAboutWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutWhy(TeacherStudentsScene):
    def construct(self):
        circle = Circle(radius=2, color=YELLOW)
        circle.next_to(self.teacher, UL)
        ke_conservation = OldTex(
            "\\frac{1}{2}m_1 v_1^2 + "
            "\\frac{1}{2}m_2 v_2^2 = \\text{const.}"
        )
        ke_conservation.move_to(circle)

        self.student_says("But why?")
        self.play_student_changes(
            "erm", "raise_left_hand", "sassy",
            added_anims=[self.teacher.change, "happy"]
        )
        self.wait()
        self.play(
            ShowCreation(circle),
            RemovePiCreatureBubble(self.students[1]),
            self.teacher.change, "raise_right_hand",
        )
        self.play_all_student_changes(
            "pondering", look_at=circle
        )
        self.wait(2)
        self.play(
            Write(ke_conservation),
            circle.stretch, 1.5, 0,
        )
        self.play_all_student_changes("confused")
        self.look_at(circle)
        self.wait(3)
