# ==============================================================================
# Scene:      Question5
# Source:     videos/_2018/sphere_area.py (lines 3436-3445)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Question5.py Question5 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Question5(Scene):
    def construct(self):
        question = OldTexText(
            """
            Question \\#5: Why does this imply that the \\\\
            shadow is $\\frac{1}{4}$ the surface area?
            """
        )
        self.play(FadeInFromDown(question))
        self.wait()
