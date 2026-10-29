# ==============================================================================
# Scene:      HoldOffUntilEnd
# Source:     videos/_2022/borwein/supplements.py (lines 98-106)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HoldOffUntilEnd.py HoldOffUntilEnd -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HoldOffUntilEnd(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("I'll mention the\ntrick at the end"),
            self.change_students("confused", "hesitant", "maybe", look_at=self.screen)
        )
        self.wait()
        self.teacher_says("But first...", target_mode="tease")
        self.wait()
