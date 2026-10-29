# ==============================================================================
# Scene:      ConstrastResultsWrapper
# Source:     videos/_2022/wordle/scenes.py (lines 3240-3249)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConstrastResultsWrapper.py ConstrastResultsWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConstrastResultsWrapper(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        screens = Rectangle(4, 3).replicate(2)
        screens.arrange(RIGHT, buff=SMALL_BUFF)
        screens.set_width(FRAME_WIDTH - 1)
        screens.set_stroke(WHITE, 1)
        screens.set_fill(BLACK, 1)
        screens.move_to(DOWN)
        self.add(screens)
