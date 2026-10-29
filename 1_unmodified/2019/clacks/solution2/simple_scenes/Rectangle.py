# ==============================================================================
# Scene:      Rectangle
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 89-93)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Rectangle.py Rectangle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Rectangle(Scene):
    def construct(self):
        rect = ScreenRectangle(height=FRAME_HEIGHT - 0.25)
        rect.set_stroke(WHITE, 6)
        self.add(rect)
