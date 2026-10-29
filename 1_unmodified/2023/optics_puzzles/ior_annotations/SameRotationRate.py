# ==============================================================================
# Scene:      SameRotationRate
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1550-1563)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SameRotationRate.py SameRotationRate -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SameRotationRate(InteractiveScene):
    def construct(self):
        # Test
        words = Text("Same rate\nof rotation", font_size=60)
        words.to_edge(RIGHT)
        arrows = VGroup(*(
            Arrow(words.get_corner(corner), y * UP + 1.25 * RIGHT, buff=0.2)
            for y, corner in zip([2.75, 0, -2.75], [UL, LEFT, DL])
        ))
        self.play(
            Write(words),
            LaggedStartMap(GrowArrow, arrows)
        )
        self.wait()
