# ==============================================================================
# Scene:      ButIHaveNoExperience
# Source:     videos/_2021/some1.py (lines 299-313)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ButIHaveNoExperience.py ButIHaveNoExperience -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ButIHaveNoExperience(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("But I have no\\\\experience!"),
            index=0,
            target_mode="pleading",
        )
        self.play_student_changes(
            "pleading", "pondering", "pondering",
            look_at=self.students[0].bubble,
        )
        self.students[0].look_at(self.teacher.eyes)
        self.play(self.teacher.change("tease", self.students[0].eyes))

        self.wait(4)
