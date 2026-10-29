# ==============================================================================
# Scene:      WriteSquares
# Source:     videos/_2026/print_gallery/misc_scenes.py (lines 589-595)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteSquares.py WriteSquares -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteSquares(InteractiveScene):
    def construct(self):
        squaresText = TexText(
            "Squares!",
            font_size=150
        ).set_color(WHITE).set_stroke(width=10, color=BLACK, behind=True)
        self.play(Write(squaresText, stroke_color=WHITE), run_time=2)
