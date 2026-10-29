# ==============================================================================
# Scene:      ObviouslyOne
# Source:     videos/_2022/puzzles/subsets.py (lines 4878-4888)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ObviouslyOne.py ObviouslyOne -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ObviouslyOne(TeacherStudentsScene):
    def construct(self):
        eq = Tex("z^5 = 1", font_size=72)
        self.teacher_holds_up(eq)
        self.wait()
        self.student_says(
            OldTexText("Obviously $z = 1$!"), target_mode="angry",
            bubble_config=dict(direction=RIGHT),
            added_anims=[self.change_students("sassy", "hesitant")]
        )
        self.wait(4)
