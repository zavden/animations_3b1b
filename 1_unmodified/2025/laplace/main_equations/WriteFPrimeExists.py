# ==============================================================================
# Scene:      WriteFPrimeExists
# Source:     videos/_2025/laplace/main_equations.py (lines 1660-1664)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteFPrimeExists.py WriteFPrimeExists -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteFPrimeExists(InteractiveScene):
    def construct(self):
        words = TexText("$f'(z)$ Exists")
        self.play(Write(words))
        self.wait()
