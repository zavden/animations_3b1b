# ==============================================================================
# Scene:      DrawSphere
# Source:     videos/_2018/borsuk_addition.py (lines 1093-1107)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl DrawSphere.py DrawSphere -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class DrawSphere(SpecialThreeDScene):
    def construct(self):
        sphere = self.get_sphere()
        sphere.shift(IN)
        question = OldTexText("What \\emph{is} a sphere?")
        question.set_width(FRAME_WIDTH - 3)
        question.to_edge(UP)
        self.move_camera(phi=70 * DEGREES, run_time=0)
        self.begin_ambient_camera_rotation()
        self.add_fixed_in_frame_mobjects(question)
        self.play(
            Write(sphere),
            FadeInFromDown(question)
        )
        self.wait(4)
