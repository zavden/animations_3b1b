# ==============================================================================
# Scene:      MovingBrace
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 30-39)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MovingBrace.py MovingBrace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MovingBrace(InteractiveScene):
    def construct(self):
        # Test
        brace = Brace(ScreenRectangle(height=FRAME_HEIGHT / 2), UP)
        brace.set_y(2.5).to_edge(LEFT, buff=0.75)

        self.play(GrowFromCenter(brace))
        self.wait()
        self.play(brace.animate.to_edge(RIGHT, buff=0.75))
        self.wait()
