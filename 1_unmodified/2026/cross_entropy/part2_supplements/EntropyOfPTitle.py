# ==============================================================================
# Scene:      EntropyOfPTitle
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 211-218)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EntropyOfPTitle.py EntropyOfPTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EntropyOfPTitle(InteractiveScene):
    def construct(self):
        title = Text("Entropy of P", font_size=72, t2c={"P": GREEN})
        equation = Tex(R"\sum_i p_i (-\log_2 p_i)", t2c={"p_i": GREEN})
        title.to_edge(UP)
        equation.next_to(title, DOWN)

        self.add(title, equation)
