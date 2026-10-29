# ==============================================================================
# Scene:      HowIsThatHelpful
# Source:     videos/_2024/puzzles/supplements.py (lines 354-370)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowIsThatHelpful.py HowIsThatHelpful -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowIsThatHelpful(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        self.play(
            stds[2].says(
                "How is that\nhelpful?",
                mode="raise_left_hand",
                look_at=morty.eyes,
                bubble_direction=LEFT,
            ),
            stds[1].change("confused", self.screen),
            stds[0].change("pondering", self.screen),
            morty.change("guilty")
        )
        self.wait(3)
