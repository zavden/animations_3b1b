# ==============================================================================
# Scene:      IndicationArrow
# Source:     videos/_2020/sir.py (lines 2472-2482)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IndicationArrow.py IndicationArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IndicationArrow(Scene):
    def construct(self):
        vect = Vector(
            0.5 * DR,
            max_tip_length_to_length_ratio=0.4,
            max_stroke_width_to_length_ratio=10,
            stroke_width=5,
        )
        vect.set_color(YELLOW)
        self.play(GrowArrow(vect))
        self.play(FadeOut(vect))
