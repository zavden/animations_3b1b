# ==============================================================================
# Scene:      ThinkAboutWhy
# Source:     videos/_2026/print_gallery/supplements.py (lines 539-547)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThinkAboutWhy.py ThinkAboutWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThinkAboutWhy(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("Think about\nwhy", mode="happy"),
            self.change_students("pondering", "thinking", "pondering", look_at=self.screen)
        )
        self.wait()
        self.play(self.teacher.change("raise_right_hand"))
        self.wait(5)
