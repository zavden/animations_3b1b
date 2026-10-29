# ==============================================================================
# Scene:      VEquation
# Source:     videos/_2023/moser_reboot/main.py (lines 1004-1009)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VEquation.py VEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VEquation(InteractiveScene):
    def construct(self):
        eq = Tex(R"V = n + {n \choose 4}")
        eq.to_corner(UL)
        self.play(Write(eq))
        self.wait()
