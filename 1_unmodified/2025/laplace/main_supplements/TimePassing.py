# ==============================================================================
# Scene:      TimePassing
# Source:     videos/_2025/laplace/main_supplements.py (lines 786-790)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TimePassing.py TimePassing -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TimePassing(InteractiveScene):
    def construct(self):
        clock = Clock()
        self.add(clock)
        self.play(ClockPassesTime(clock, hours_passed=2, run_time=10))
