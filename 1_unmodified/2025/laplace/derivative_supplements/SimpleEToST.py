# ==============================================================================
# Scene:      SimpleEToST
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 68-71)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleEToST.py SimpleEToST -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleEToST(InteractiveScene):
    def construct(self):
        tex = Tex(R"e^{st}", t2c={"s": YELLOW, "t": GREY_A}, font_size=120)
        self.add(tex)
