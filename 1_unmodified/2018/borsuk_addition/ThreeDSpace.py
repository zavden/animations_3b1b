# ==============================================================================
# Scene:      ThreeDSpace
# Source:     videos/_2018/borsuk_addition.py (lines 1142-1166)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl ThreeDSpace.py ThreeDSpace -w -m --fps 15
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

class ThreeDSpace(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-130 * DEGREES)
        self.begin_ambient_camera_rotation()

        density = 1
        radius = 3
        lines = VGroup(*[
            VGroup(*[
                Line(
                    radius * IN, radius * OUT,
                    stroke_color=WHITE,
                    stroke_width=1,
                    stroke_opacity=0.5,
                ).shift(x * RIGHT + y * UP)
                for x in np.arange(-radius, radius + density, density)
                for y in np.arange(-radius, radius + density, density)
            ]).rotate(n * 120 * DEGREES, axis=[1, 1, 1])
            for n in range(3)
        ])

        self.play(Write(lines))
        self.wait(30)
