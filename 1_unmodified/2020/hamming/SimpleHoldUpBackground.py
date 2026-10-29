# ==============================================================================
# Scene:      SimpleHoldUpBackground
# Source:     videos/_2020/hamming.py (lines 6296-6302)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleHoldUpBackground.py SimpleHoldUpBackground -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleHoldUpBackground(TeacherStudentsScene):
    def construct(self):
        self.play(self.teacher.change, "raise_right_hand", 3 * UP)
        self.play_student_changes("pondering", "thinking", "tease", look_at=3 * UP)
        self.wait(4)
        self.play_student_changes("tease", "hesitant", "happy", look_at=3 * UP)
        self.wait(5)
