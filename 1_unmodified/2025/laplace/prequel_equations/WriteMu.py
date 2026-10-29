# ==============================================================================
# Scene:      WriteMu
# Source:     videos/_2025/laplace/prequel_equations.py (lines 698-710)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteMu.py WriteMu -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteMu(InteractiveScene):
    def construct(self):
        sym = Tex(R"\mu")
        rect = SurroundingRectangle(sym, buff=0.05)
        rect.set_stroke(YELLOW, 2)
        mu = TexText("``Mu''")
        mu.set_color(YELLOW)
        mu.next_to(rect, DOWN)
        self.play(
            Write(mu),
            ShowCreation(rect)
        )
        self.wait()
