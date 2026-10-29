# ==============================================================================
# Scene:      AngleLabel
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 950-957)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AngleLabel.py AngleLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AngleLabel(InteractiveScene):
    def construct(self):
        # Test
        arc = Arc(180 * DEG, -10 * DEG, radius=2)
        theta = Tex(R"\theta")
        theta.next_to(arc, LEFT, aligned_edge=DOWN, buff=SMALL_BUFF)

        self.add(arc, theta)
