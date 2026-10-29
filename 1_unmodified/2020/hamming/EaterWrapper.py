# ==============================================================================
# Scene:      EaterWrapper
# Source:     videos/_2020/hamming.py (lines 1130-1149)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EaterWrapper.py EaterWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EaterWrapper(Scene):
    def construct(self):
        bg_rect = FullScreenRectangle()
        bg_rect.set_fill(GREY_E, 1)
        bg_rect.set_stroke(BLACK, 0)
        self.add(bg_rect)

        title = OldTexText("Ben Eater implementing Hamming codes")
        title.set_width(FRAME_WIDTH - 2)
        title.to_edge(UP)
        self.add(title)

        screen_rect = ScreenRectangle()
        screen_rect.set_fill(BLACK, 1)
        screen_rect.set_height(6)
        screen_rect.next_to(title, DOWN, MED_LARGE_BUFF)
        self.add(screen_rect)

        self.add(AnimatedBoundary(screen_rect))
        self.wait(16)
