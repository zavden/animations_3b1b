# ==============================================================================
# Scene:      WriteSPlane
# Source:     videos/_2025/laplace/prequel_equations.py (lines 588-593)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteSPlane.py WriteSPlane -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteSPlane(InteractiveScene):
    def construct(self):
        title = Text("S-plane", font_size=72)
        title.set_color(YELLOW)
        self.play(Write(title))
        self.wait()
