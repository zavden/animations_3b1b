# ==============================================================================
# Scene:      SnellPuzzle
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 375-391)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SnellPuzzle.py SnellPuzzle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SnellPuzzle(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Puzzle", font_size=60).set_color(YELLOW)
        underline = Underline(title, stretch_factor=2, stroke_color=YELLOW)
        puzzle = TexText(R"""
            Can you find an equation \\
            relating $\lambda_1$, $\lambda_2$, $\theta_1$ and $\theta_2$?
        """)
        puzzle.next_to(underline, DOWN, buff=0.5)
        group = VGroup(title, underline, puzzle)
        rect = SurroundingRectangle(group, buff=0.25)
        rect.set_fill(BLACK, 1)
        rect.set_stroke(WHITE, 0)
        group.add_to_back(rect)
        group.to_corner(UL)
        self.add(group)
