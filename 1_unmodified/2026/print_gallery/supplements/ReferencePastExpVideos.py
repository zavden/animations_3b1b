# ==============================================================================
# Scene:      ReferencePastExpVideos
# Source:     videos/_2026/print_gallery/supplements.py (lines 516-536)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferencePastExpVideos.py ReferencePastExpVideos -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferencePastExpVideos(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)

        # Test
        morty = self.teacher
        stds = self.students
        self.play(
            stds[1].says("Why?", mode="confused", look_at=2 * UR),
            stds[2].change("erm", look_at=2 * UR),
            stds[0].change("pondering", look_at=2 * UL),
            morty.change("tease"),
        )
        self.wait(3)
        self.play(
            morty.change("raise_left_hand", look_at=3 * UR),
            stds[1].debubble("pondering", look_at=3 * UR),
            stds[2].change("tease"),
            stds[0].change("thinking"),
        )
        self.wait(5)
