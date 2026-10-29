# ==============================================================================
# Scene:      ExpressAnger
# Source:     videos/_2022/borwein/supplements.py (lines 12-25)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpressAnger.py ExpressAnger -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExpressAnger(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        self.students[1].change_mode("maybe")
        self.play(
            self.teacher.change("raise_left_hand", look_at=3 * RIGHT + UP),
            self.change_students("pondering", "confused", "thinking", look_at=3 * RIGHT + UP)
        )
        self.wait(2)
        self.play(
            self.teacher.change("tease", look_at=3 * RIGHT + UP),
            self.change_students("angry", "erm", "pleading", look_at=3 * RIGHT + UP)
        )
        self.wait(5)
