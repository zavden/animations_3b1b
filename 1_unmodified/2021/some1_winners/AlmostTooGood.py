# ==============================================================================
# Scene:      AlmostTooGood
# Source:     videos/_2021/some1_winners.py (lines 664-672)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AlmostTooGood.py AlmostTooGood -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AlmostTooGood(TeacherStudentsScene):
    def construct(self):
        self.pi_creatures.flip().flip()
        self.teacher_says(
            OldTexText("Almost \\emph{too} good"),
            look_at=self.students[2].eyes,
            added_anims=[self.change_students("happy", "tease", "hesitant")],
        )
        self.wait(4)
