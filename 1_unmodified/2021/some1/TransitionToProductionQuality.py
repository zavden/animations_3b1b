# ==============================================================================
# Scene:      TransitionToProductionQuality
# Source:     videos/_2021/some1.py (lines 1064-1077)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TransitionToProductionQuality.py TransitionToProductionQuality -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TransitionToProductionQuality(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.students[0].change("pondering"),
            self.students[2].change("pondering"),
        )
        self.student_says(
            OldTexText("What parts of\\\\production quality matter?"),
            index=1
        )
        self.play(
            self.teacher.change("happy"),
        )
        self.wait(3)
