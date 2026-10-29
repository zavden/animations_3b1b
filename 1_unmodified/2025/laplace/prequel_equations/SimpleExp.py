# ==============================================================================
# Scene:      SimpleExp
# Source:     videos/_2025/laplace/prequel_equations.py (lines 1619-1621)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleExp.py SimpleExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleExp(InteractiveScene):
    def construct(self):
        self.add(Tex(R"e^{st}", t2c={"s": YELLOW}, font_size=60))
