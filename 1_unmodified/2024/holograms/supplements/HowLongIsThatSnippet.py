# ==============================================================================
# Scene:      HowLongIsThatSnippet
# Source:     videos/_2024/holograms/supplements.py (lines 702-708)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowLongIsThatSnippet.py HowLongIsThatSnippet -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowLongIsThatSnippet(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("How long is\nthat snippet?"),
            self.change_students("happy", "tease", "thinking", look_at=self.screen)
        )
        self.wait(3)
