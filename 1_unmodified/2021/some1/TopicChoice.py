# ==============================================================================
# Scene:      TopicChoice
# Source:     videos/_2021/some1.py (lines 156-163)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TopicChoice.py TopicChoice -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TopicChoice(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("What kind of\\\\topics?"),
            added_anims=[self.teacher.change("tease")],
            index=1,
        )
        self.wait(3)
