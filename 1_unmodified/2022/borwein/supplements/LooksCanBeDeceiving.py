# ==============================================================================
# Scene:      LooksCanBeDeceiving
# Source:     videos/_2022/borwein/supplements.py (lines 28-34)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LooksCanBeDeceiving.py LooksCanBeDeceiving -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LooksCanBeDeceiving(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("Looks can be\ndeceiving", mode="tease"),
            self.change_students("angry", "erm", "pleading", look_at=self.screen)
        )
        self.wait(3)
