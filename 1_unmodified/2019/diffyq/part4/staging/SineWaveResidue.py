# ==============================================================================
# Scene:      SineWaveResidue
# Source:     videos/_2019/diffyq/part4/staging.py (lines 1138-1153)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SineWaveResidue.py SineWaveResidue -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SineWaveResidue(Scene):
    def construct(self):
        f = 2
        wave = FunctionGraph(
            lambda x: np.cos(-0.1 * f * TAU * x),
            x_min=0,
            x_max=20,
            color=YELLOW,
        )
        wave.next_to(LEFT_SIDE, LEFT, buff=0)
        time = 10
        self.play(
            wave.shift, time * RIGHT,
            run_time=f * time,
            rate_func=linear,
        )
