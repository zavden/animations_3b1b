# ==============================================================================
# Scene:      KeyStep
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 457-466)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KeyStep.py KeyStep -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class KeyStep(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.teacher.says("This is the\nkey step"),
            self.change_students("pondering", "thinking", "erm", look_at=self.screen)
        )
        self.wait()
        self.play(self.change_students("thinking", "well", "pondering", look_at=self.screen))
        self.wait(3)
