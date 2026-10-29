# ==============================================================================
# Scene:      Arrows
# Source:     videos/_2024/puzzles/max_rand.py (lines 569-575)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Arrows.py Arrows -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Arrows(InteractiveScene):
    def construct(self):
        arrows = Vector(DOWN, thickness=5).replicate(3)
        arrows.arrange(RIGHT, buff=1.0)
        arrows.set_fill(YELLOW)
        self.play(LaggedStartMap(GrowArrow, arrows))
        self.wait()
