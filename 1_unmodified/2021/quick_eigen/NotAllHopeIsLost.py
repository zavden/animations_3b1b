# ==============================================================================
# Scene:      NotAllHopeIsLost
# Source:     videos/_2021/quick_eigen.py (lines 2060-2068)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NotAllHopeIsLost.py NotAllHopeIsLost -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NotAllHopeIsLost(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            OldTexText("There's still a\\\\good example here"),
            target_mode="speaking",
            bubble_config={"height": 3, "width": 4},
            added_anims=[self.change_students("erm", "sassy", "hesitant")],
        )
        self.wait(2)
