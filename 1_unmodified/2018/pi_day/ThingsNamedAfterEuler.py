# ==============================================================================
# Scene:      ThingsNamedAfterEuler
# Source:     videos/_2018/pi_day.py (lines 727-745)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThingsNamedAfterEuler.py ThingsNamedAfterEuler -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThingsNamedAfterEuler(Scene):
    def construct(self):
        group = VGroup(*list(map(TexText, [
            "Euler's formula (Complex analysis)",
            "Euler's formula (Graph theory)",
            "Euler's formula (Mechanical engineering)",
            "Euler's formula (Analytical number theory)",
            "Euler's formula (Continued fractions)",
            "Euler-Lagrance equations (mechanics)",
            "Euler number (topology)",
            "Euler equations (fluid dynamics)",
            "Euler angles (rigid-body mechanics)",
            "Euler totient function (number theory)",
        ])))
        group.arrange(DOWN, aligned_edge = LEFT)
        group.set_height(FRAME_HEIGHT - 1)

        self.play(LaggedStartMap(FadeIn, group, lag_ratio = 0.2, run_time = 12))
        self.wait()
