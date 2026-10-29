# ==============================================================================
# Scene:      AskWhy
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 451-472)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhy.py AskWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskWhy(TeacherStudentsScene):
    def construct(self):
        # Test
        self.remove(self.background)
        stds = self.students
        morty = self.teacher

        self.play(
            stds[1].says("Wait, why?", mode="confused", look_at=self.screen),
            stds[0].change("pondering", self.screen),
            stds[2].change("pondering", self.screen),
            morty.change("tease")
        )
        self.wait(1)
        self.play(
            morty.change("raise_left_hand", 6 * UR),
            FadeOut(stds[1].bubble),
            self.change_students("pondering", "erm", "thinking", look_at=6 * UR)
        )
        self.wait(5)
        self.play(LaggedStartMap(FadeOut, self.pi_creatures, shift=DOWN, lag_ratio=0.1))
        self.wait()
