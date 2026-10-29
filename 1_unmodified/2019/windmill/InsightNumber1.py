# ==============================================================================
# Scene:      InsightNumber1
# Source:     videos/_2019/windmill.py (lines 2866-2875)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InsightNumber1.py InsightNumber1 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InsightNumber1(Scene):
    def construct(self):
        words = OldTexText(
            "Key insight 1: ",
            "\\# Points on either side is constant"
        )
        words[0].set_color(YELLOW)
        words.set_width(FRAME_WIDTH - 1)
        self.play(FadeInFromDown(words))
        self.wait()
