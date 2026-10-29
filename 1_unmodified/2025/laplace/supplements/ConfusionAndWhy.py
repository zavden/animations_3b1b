# ==============================================================================
# Scene:      ConfusionAndWhy
# Source:     videos/_2025/laplace/supplements.py (lines 221-246)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConfusionAndWhy.py ConfusionAndWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConfusionAndWhy(TeacherStudentsScene):
    def construct(self):
        # Test
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(200)
        morty = self.teacher
        stds = self.students

        q_marks = Tex(R"???").replicate(3)
        q_marks.space_out_submobjects(1.5)
        for mark, student in zip(q_marks, stds):
            mark.next_to(student, UP, MED_SMALL_BUFF)
        self.play(
            self.change_students("confused", "pondering", "pleading", look_at=self.screen),
            FadeIn(q_marks, 0.2 * UP, lag_ratio=0.05),
            morty.change("raise_right_hand")
        )
        self.wait(3)
        self.play(morty.change("raise_left_hand", look_at=3 * UR))
        self.play(
            self.change_students("erm", "thinking", "hesitant", look_at=morty.get_top() + 2 * UP),
            FadeOut(q_marks)
        )
        self.wait(4)
        self.play(self.change_students("pondering"))
        self.wait(3)
