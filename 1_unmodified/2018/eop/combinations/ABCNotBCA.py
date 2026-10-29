# ==============================================================================
# Scene:      ABCNotBCA
# Source:     videos/_2018/eop/combinations.py (lines 3249-3258)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ABCNotBCA.py ABCNotBCA -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ABCNotBCA(Scene):
    def construct(self):
        words = OldTexText("If order mattered:")
        equation = OldTexText("(A, B, C) $\\ne$ (B, C, A)")
        equation.set_color(YELLOW)
        equation.next_to(words, DOWN)
        group = VGroup(words, equation)
        group.set_width(FRAME_WIDTH - 1)
        group.to_edge(DOWN)
        self.add(words, equation)
