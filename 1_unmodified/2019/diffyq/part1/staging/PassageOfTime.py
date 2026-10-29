# ==============================================================================
# Scene:      PassageOfTime
# Source:     videos/_2019/diffyq/part1/staging.py (lines 2930-2941)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PassageOfTime.py PassageOfTime -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PassageOfTime(Scene):
    def construct(self):
        clock = Clock()
        clock[0].set_color(BLUE)
        clock.set_stroke(width=1)
        clock.scale(0.8)
        clock.to_corner(UL)
        passage = ClockPassesTime(
            clock,
            hours_passed=48,
        )
        self.play(passage, run_time=10)
