# ==============================================================================
# Scene:      Reinvention
# Source:     videos/_2020/hamming.py (lines 1113-1127)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Reinvention.py Reinvention -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Reinvention(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.change, "raise_right_hand",
            self.change_students(*3 * ["pondering"]),
        )
        self.wait(3)
        self.student_says(
            "I see where\\\\this is going",
            index=0,
            target_mode="tease",
        )
        self.look_at(self.students[0].bubble)
        self.play(self.students[0].change, "thinking")
        self.wait(6)
