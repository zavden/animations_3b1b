# ==============================================================================
# Scene:      OverOrUnderExplain
# Source:     videos/_2025/grover/clarification.py (lines 1294-1314)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OverOrUnderExplain.py OverOrUnderExplain -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OverOrUnderExplain(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change("shruggie"),
            self.change_students("pondering", "pondering", "pondering", look_at=self.screen),
        )
        self.wait(2)
        self.play(LaggedStart(
            stds[2].change("erm", look_at=morty.eyes),
            morty.change("hesitant", look_at=self.students),
        ))
        self.wait(2)
        self.play(
            morty.change("raise_right_hand"),
            self.change_students("hesitant", "well", "confused", look_at=3 * UR)
        )
        self.wait(5)
