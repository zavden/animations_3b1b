# ==============================================================================
# Scene:      TheresADeeperIssue
# Source:     videos/_2024/holograms/supplements.py (lines 1165-1178)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TheresADeeperIssue.py TheresADeeperIssue -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TheresADeeperIssue(TeacherStudentsScene):
    def construct(self):
        for std in self.students:
            std.change_mode("pondering")
            std.look_at(self.screen)
        self.play(
            self.teacher.says("There's a\ndeeper issue"),
            self.change_students("erm", "guilty", "hesitant", look_at=self.teacher.eyes)
        )
        self.wait(2)
        self.play(
            self.change_students("pondering", "pondering", 'pondering', look_at=self.screen)
        )
        self.wait(2)
