# ==============================================================================
# Scene:      IntegralOverlay
# Source:     videos/_2021/shadows.py (lines 3992-4003)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntegralOverlay.py IntegralOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntegralOverlay(Scene):
    def construct(self):
        integral = OldTex("\\int_0^\\pi")
        integral.set_color(YELLOW)

        self.play(Write(integral, run_time=2))
        self.play(integral.animate.set_color(WHITE))
        self.play(LaggedStart(*(
            FlashAround(sm, time_width=3)
            for sm in integral[0][:0:-1]
        ), lag_ratio=0.5, run_time=3))
        self.wait()
