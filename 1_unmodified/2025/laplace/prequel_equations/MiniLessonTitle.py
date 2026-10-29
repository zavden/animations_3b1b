# ==============================================================================
# Scene:      MiniLessonTitle
# Source:     videos/_2025/laplace/prequel_equations.py (lines 132-137)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MiniLessonTitle.py MiniLessonTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MiniLessonTitle(InteractiveScene):
    def construct(self):
        title = Text("Visualizing complex exponents", font_size=72)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
