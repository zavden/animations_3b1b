# ==============================================================================
# Scene:      KIsSomeConstant
# Source:     videos/_2025/laplace/prequel_equations.py (lines 686-695)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KIsSomeConstant.py KIsSomeConstant -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class KIsSomeConstant(InteractiveScene):
    def construct(self):
        rect = SurroundingRectangle(Text("k"), buff=0.05)
        rect.set_stroke(YELLOW, 2)
        words = Text("Some constant", font_size=24)
        words.next_to(rect, UP, SMALL_BUFF)
        words.match_color(rect)

        self.play(ShowCreation(rect), FadeIn(words))
        self.wait()
