# ==============================================================================
# Scene:      DefineI
# Source:     videos/_2025/laplace/prequel_equations.py (lines 391-395)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineI.py DefineI -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefineI(InteractiveScene):
    def construct(self):
        eq = Tex(R"i = \sqrt{-1}", t2c={"i": YELLOW}, font_size=90)
        self.play(Write(eq))
        self.wait()
