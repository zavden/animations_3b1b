# ==============================================================================
# Scene:      GiantCross
# Source:     videos/_2019/diffyq/part3/staging.py (lines 1081-1096)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GiantCross.py GiantCross -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GiantCross(Scene):
    def construct(self):
        rect = FullScreenFadeRectangle()
        cross = Cross(rect)
        cross.set_stroke(RED, 25)

        words = OldTexText("This wouldn't\\\\happen!")
        words.scale(2)
        words.set_color(RED)
        words.to_edge(UP)

        self.play(
            FadeInFromDown(words),
            ShowCreation(cross),
        )
        self.wait()
