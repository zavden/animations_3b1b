# ==============================================================================
# Scene:      RecapWrapper
# Source:     videos/_2021/quick_eigen.py (lines 325-334)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RecapWrapper.py RecapWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RecapWrapper(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        screen = ScreenRectangle(height=6.75)
        screen.set_stroke(BLUE_B, 2)
        screen.set_fill(BLACK, 1)
        screen.to_edge(DOWN, buff=0.25)
        title = Text("Quick review")
        title.to_edge(UP, buff=0.25)
        self.add(title, screen)
