# ==============================================================================
# Scene:      SameExampleWrapper
# Source:     videos/_2021/quick_eigen.py (lines 1595-1605)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SameExampleWrapper.py SameExampleWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SameExampleWrapper(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        screen = ScreenRectangle()
        screen.set_fill(BLACK, 1)
        screen.set_stroke(BLUE, 3)
        screen.set_height(6)
        screen.to_edge(DOWN)
        title = Text("Same example from before")
        title.next_to(screen, UP)
        self.add(screen, title)
