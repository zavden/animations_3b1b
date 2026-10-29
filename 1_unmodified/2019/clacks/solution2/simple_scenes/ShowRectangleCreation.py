# ==============================================================================
# Scene:      ShowRectangleCreation
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 96-101)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowRectangleCreation.py ShowRectangleCreation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowRectangleCreation(Scene):
    def construct(self):
        rect = ScreenRectangle(height=2)
        rect.set_stroke(YELLOW, 6)
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
