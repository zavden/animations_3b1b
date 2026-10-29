# ==============================================================================
# Scene:      WaitWhat
# Source:     videos/_2026/print_gallery/supplements.py (lines 613-622)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WaitWhat.py WaitWhat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WaitWhat(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        self.play(
            stds[2].says("Wait, what?", mode="confused", look_at=self.screen),
            stds[0].change("maybe", look_at=self.screen),
            stds[1].change("erm", look_at=self.screen),
            self.teacher.change("tease")
        )
        self.wait(3)
