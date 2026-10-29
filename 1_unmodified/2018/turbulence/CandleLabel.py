# ==============================================================================
# Scene:      CandleLabel
# Source:     videos/_2018/turbulence.py (lines 1210-1219)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CandleLabel.py CandleLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CandleLabel(Scene):
    def construct(self):
        word = OldTexText("Candle")
        arrow = Vector(DR, color=WHITE)
        arrow.move_to(word.get_bottom() + SMALL_BUFF * DOWN, UL)
        self.play(
            FadeInFromDown(word),
            GrowArrow(arrow)
        )
        self.wait()
