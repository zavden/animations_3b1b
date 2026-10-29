# ==============================================================================
# Scene:      TangencyAnimation
# Source:     videos/_2018/dandelin.py (lines 885-900)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TangencyAnimation.py TangencyAnimation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TangencyAnimation(Scene):
    def construct(self):
        rings = VGroup(*[
            Circle(color=YELLOW, stroke_width=3, radius=0.5)
            for x in range(5)
        ])
        for ring in rings:
            ring.save_state()
            ring.scale(0)
            ring.saved_state.set_stroke(width=0)

        self.play(LaggedStartMap(
            Restore, rings,
            run_time=2,
            lag_ratio=0.7
        ))
