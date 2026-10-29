# ==============================================================================
# Scene:      SorryWhat
# Source:     videos/_2026/print_gallery/supplements.py (lines 187-198)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SorryWhat.py SorryWhat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SorryWhat(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        stds = self.students
        self.screen.center().to_edge(UP)
        self.play(
            stds[0].says("I'm sorry, what?", mode="maybe", look_at=self.screen),
            stds[2].change("maybe", look_at=self.screen),
            stds[1].change("confused", look_at=self.screen),
            self.teacher.change("tease")
        )
        self.wait(3)
