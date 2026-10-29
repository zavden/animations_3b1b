# ==============================================================================
# Scene:      HowAreYouFindingTheBest
# Source:     videos/_2022/wordle/footnote.py (lines 483-497)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowAreYouFindingTheBest.py HowAreYouFindingTheBest -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowAreYouFindingTheBest(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("What exactly is this\\\\``final analysis''?"),
            index=0,
        )
        self.play(
            self.students[1].change("pondering"),
            self.students[2].change("raise_left_hand"),
            self.teacher.change("happy")
        )
        self.wait(2)

        self.teacher_says(OldTexText("I'm glad\\\\you asked!"), target_mode="hooray")
        self.wait(3)
