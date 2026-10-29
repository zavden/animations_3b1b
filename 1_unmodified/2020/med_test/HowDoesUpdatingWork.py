# ==============================================================================
# Scene:      HowDoesUpdatingWork
# Source:     videos/_2020/med_test.py (lines 5702-5745)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowDoesUpdatingWork.py HowDoesUpdatingWork -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowDoesUpdatingWork(TeacherStudentsScene):
    def construct(self):
        students = self.students
        teacher = self.teacher

        self.student_says(
            "Where are these\\\\numbers coming\\\\from?",
            target_mode="raise_right_hand"
        )
        self.play(
            teacher.change, "happy",
            self.change_students("confused", "erm", "raise_right_hand"),
        )
        self.look_at(self.screen)
        self.wait(3)

        sample_pop = OldTexText("Sample populations (most intuitive)")
        bayes_factor = OldTexText("Bayes' factor (most fun)")
        for words in sample_pop, bayes_factor:
            words.move_to(self.hold_up_spot, DOWN)
            words.shift_onto_screen()

        bayes_factor.set_fill(YELLOW)

        self.play(
            RemovePiCreatureBubble(students[2]),
            teacher.change, "raise_right_hand",
            FadeIn(sample_pop, shift=UP, scale=1.5),
            self.change_students(
                "pondering", "thinking", "pondering",
                look_at=sample_pop,
            )
        )
        self.wait(2)
        self.play(
            FadeIn(bayes_factor, shift=UP, scale=1.5),
            sample_pop.shift, UP,
            teacher.change, "hooray",
            self.change_students(
                "thinking", "confused", "erm",
            )
        )
        self.look_at(bayes_factor)
        self.wait(3)
