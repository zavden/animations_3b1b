# ==============================================================================
# Scene:      ShowLeftArrow
# Source:     videos/_2019/clacks/question.py (lines 721-726)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowLeftArrow.py ShowLeftArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowLeftArrow(Scene):
    def construct(self):
        arrow = Vector(2 * LEFT, color=RED)
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(FadeOut(arrow))
