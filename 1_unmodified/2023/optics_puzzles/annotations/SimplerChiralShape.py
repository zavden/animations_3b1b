# ==============================================================================
# Scene:      SimplerChiralShape
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 1149-1196)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl SimplerChiralShape.py SimplerChiralShape -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2023/optics_puzzles/objects.py -----

class TwistedRibbon(ParametricSurface):
    def __init__(
        self,
        axes,
        amplitude,
        twist_rate,
        start_point=(0, 0, 0),
        color=WHITE,
        opacity=0.4,
        resolution=(101, 11),
    ):
        super().__init__(
            lambda u, v: axes.c2p(
                u,
                v * amplitude * np.sin(TAU * twist_rate * u),
                v * amplitude * np.cos(TAU * twist_rate * u)
            ),
            u_range=axes.x_range[:2],
            v_range=(-1, 1),
            color=color,
            opacity=opacity,
            resolution=resolution,
            preferred_creation_axis=0,
        )
        self.shift(axes.c2p(*start_point) - axes.get_origin())



# ----- From _2023/optics_puzzles/annotations.py -----

class SimplerChiralShape(InteractiveScene):
    default_frame_orientation = (0, 70)

    def construct(self):
        # Ribbon
        frame = self.frame
        frame.set_field_of_view(1 * DEGREES)
        axes = ThreeDAxes((-3, 3))
        ribbon = TwistedRibbon(axes, amplitude=1, twist_rate=-0.35)
        ribbon.rotate(PI / 2, DOWN)
        ribbon.set_color(RED)
        ribbon.set_opacity(0.9)
        ribbon.set_shading(0.5, 0.5, 0.5)
        ribbon.set_sort_to_camera()
        ribbon.set_x(-4)

        mirror_image = ribbon.copy()
        mirror_image.stretch(-1, 0)
        mirror_image.set_x(-ribbon.get_x())
        mirror_image.set_color(YELLOW_C)
        mirror_image.set_opacity(0.9)

        # Title
        spiral_name = Text("Spiral")
        mirror_name = Text("Mirror image")
        for name, mob in [(spiral_name, ribbon), (mirror_name, mirror_image)]:
            name.fix_in_frame()
            name.to_edge(UP)
            name.match_x(mob)

        self.play(
            FadeIn(spiral_name, 0.5 * UP),
            ShowCreation(ribbon, run_time=3),
        )
        self.wait()
        self.play(
            ReplacementTransform(ribbon.copy().shift(0.1 * DOWN), mirror_image),
            FadeTransformPieces(spiral_name.copy(), mirror_name),
        )
        self.wait()

        # Reorient
        r_copy = ribbon.copy()
        self.play(r_copy.animate.next_to(mirror_image, LEFT))
        self.play(Rotate(r_copy, PI, RIGHT, run_time=2))
        self.play(Rotate(r_copy, PI, OUT, run_time=2))
        self.play(Rotate(r_copy, PI, UP, run_time=2))
        self.wait()
