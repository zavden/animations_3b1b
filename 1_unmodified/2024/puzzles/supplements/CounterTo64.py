# ==============================================================================
# Scene:      CounterTo64
# Source:     videos/_2024/puzzles/supplements.py (lines 117-122)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CounterTo64.py CounterTo64 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CounterTo64(InteractiveScene):
    def construct(self):
        value = Integer(64)
        value.scale(2)
        self.play(CountInFrom(value, 0), rate_func=linear, run_time=12)
        self.wait()
