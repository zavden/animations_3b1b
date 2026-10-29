# ==============================================================================
# Scene:      AngryStudents
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 909-916)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AngryStudents.py AngryStudents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AngryStudents(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.change_students("angry", "confused", "sassy"),
            self.teacher.change("guilty"),
        )
        self.wait(3)
