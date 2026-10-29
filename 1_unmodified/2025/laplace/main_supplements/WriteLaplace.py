# ==============================================================================
# Scene:      WriteLaplace
# Source:     videos/_2025/laplace/main_supplements.py (lines 5-10)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteLaplace.py WriteLaplace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteLaplace(InteractiveScene):
    def construct(self):
        title = Text("Laplace Transform", font_size=72)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
