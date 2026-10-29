# ==============================================================================
# Scene:      ObviouslyWrong
# Source:     videos/_2022/visual_proofs/lies.py (lines 1560-1570)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ObviouslyWrong.py ObviouslyWrong -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ObviouslyWrong(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        ss = self.students
        self.play(LaggedStart(
            ss[2].says("Obviously those\nperimeters aren't\nthe circle...", mode="sassy", look_at=self.screen, bubble_direction=LEFT),
            ss[0].change("erm", self.screen),
            ss[1].change("angry", self.screen),
            morty.change("guilty")
        ))
        self.wait(5)
