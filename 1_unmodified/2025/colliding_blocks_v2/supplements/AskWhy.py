# ==============================================================================
# Scene:      AskWhy
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 537-551)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhy.py AskWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskWhy(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.students[2].says("...why?", mode="confused", bubble_direction=LEFT, look_at=self.screen),
            self.teacher.change("tease"),
            self.change_students("pondering", "thinking", look_at=self.screen)
        )
        self.wait()
        self.play(
            self.teacher.says("Symmetry breeds\ninsight!", mode="hooray"),
            self.students[2].debubble(look_at=self.teacher.eyes)
        )
        self.play(self.change_students("thinking", "tease", "erm", self.teacher.eyes))
        self.wait()
