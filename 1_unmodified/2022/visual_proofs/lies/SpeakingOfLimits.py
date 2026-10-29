# ==============================================================================
# Scene:      SpeakingOfLimits
# Source:     videos/_2022/visual_proofs/lies.py (lines 1741-1747)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SpeakingOfLimits.py SpeakingOfLimits -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SpeakingOfLimits(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("Speaking of\nlimits..."),
            self.change_students("happy", "tease", "thinking"),
        )
        self.wait(4)
