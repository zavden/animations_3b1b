# ==============================================================================
# Scene:      LookingAtScreen
# Source:     videos/_2024/holograms/supplements.py (lines 1808-1814)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LookingAtScreen.py LookingAtScreen -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LookingAtScreen(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.change_students("confused", "pondering", "maybe", look_at=self.screen),
            self.teacher.change("well")
        )
        self.wait(5)
