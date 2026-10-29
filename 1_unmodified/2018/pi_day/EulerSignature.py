# ==============================================================================
# Scene:      EulerSignature
# Source:     videos/_2018/pi_day.py (lines 203-211)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EulerSignature.py EulerSignature -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EulerSignature(Scene):

    def construct(self):

        sig = SVGMobject(file_name = "euler-signature")

        self.play(
            Write(sig, run_time = 5)
        )
