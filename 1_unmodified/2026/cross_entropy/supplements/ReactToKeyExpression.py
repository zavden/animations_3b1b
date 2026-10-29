# ==============================================================================
# Scene:      ReactToKeyExpression
# Source:     videos/_2026/cross_entropy/supplements.py (lines 762-777)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReactToKeyExpression.py ReactToKeyExpression -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ReactToKeyExpression(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        morty.change_mode("pondering")
        self.remove(self.background)

        self.play(
            morty.change("surprised", 3 * UR),
            self.change_students("hooray", "sassy", "awe", look_at=3 * UR),
        )
        self.wait(2)
        self.play(morty.change("hooray"))
        self.wait()
        self.play(LaggedStartMap(FadeOut, self.pi_creatures, shift=DOWN, lag_ratio=0.1, run_time=1))
        self.wait()
