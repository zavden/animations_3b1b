# ==============================================================================
# Scene:      FrameForFlow
# Source:     videos/_2021/matrix_exp.py (lines 6181-6189)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FrameForFlow.py FrameForFlow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FrameForFlow(Scene):
    def construct(self):
        self.add(FullScreenRectangle(fill_color=GREY_D))
        screen_rect = ScreenRectangle()
        screen_rect.set_height(5.5)
        screen_rect.set_stroke(WHITE, 3)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.to_edge(DOWN)
        self.add(screen_rect)
