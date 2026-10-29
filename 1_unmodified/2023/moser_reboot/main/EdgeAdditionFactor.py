# ==============================================================================
# Scene:      EdgeAdditionFactor
# Source:     videos/_2023/moser_reboot/main.py (lines 1012-1020)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EdgeAdditionFactor.py EdgeAdditionFactor -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EdgeAdditionFactor(InteractiveScene):
    def construct(self):
        eq = Tex(R"""
            E = (\#\text{Original lines}) + 2(\#\text{Intersection points})
        """)
        eq["Original lines"].set_color(BLUE_B)
        eq["Intersection points"].set_color(YELLOW)
        eq.to_edge(UP)
        self.add(eq)
