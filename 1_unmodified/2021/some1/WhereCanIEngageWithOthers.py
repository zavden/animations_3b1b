# ==============================================================================
# Scene:      WhereCanIEngageWithOthers
# Source:     videos/_2021/some1.py (lines 1188-1201)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhereCanIEngageWithOthers.py WhereCanIEngageWithOthers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhereCanIEngageWithOthers(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("Where can I find\\\\others joining SoME1?"),
            index=0,
            added_anims=[
                self.students[1].change("pondering", UL),
                self.students[2].change("pondering", UL),
            ]
        )
        self.play(
            self.teacher.change("tease"),
        )
        self.wait(4)
