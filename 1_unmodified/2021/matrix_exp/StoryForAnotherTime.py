# ==============================================================================
# Scene:      StoryForAnotherTime
# Source:     videos/_2021/matrix_exp.py (lines 5049-5056)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StoryForAnotherTime.py StoryForAnotherTime -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StoryForAnotherTime(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            OldTexText("The full story\\\\takes more time."),
            bubble_config={"height": 3, "width": 3.5},
            added_anims=[self.change_students("confused", "erm", "hesitant", look_at=self.screen)]
        )
        self.wait(5)
