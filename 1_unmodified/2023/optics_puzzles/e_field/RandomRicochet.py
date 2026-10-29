# ==============================================================================
# Scene:      RandomRicochet
# Source:     videos/_2023/optics_puzzles/e_field.py (lines 1753-1809)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomRicochet.py RandomRicochet -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RandomRicochet(InteractiveScene):
    default_frame_orientation = (-36, 70)

    def construct(self):
        # Setup
        frame = self.frame
        plane, axes = self.get_plane_and_axes()
        self.add(plane, axes)

        # Light and Ball
        ball = TrueDot(radius=0.1)
        ball.make_3d()
        ball.set_color(RED)

        light = GlowDot(radius=2)
        light.move_to(5 * DOWN)
        self.add(light, ball)

        # Beams
        n_beams = 15
        beams = VGroup()
        for _ in range(n_beams):
            point = 5 * normalize(np.random.uniform(-5, 5, 3))
            beam = VMobject().set_points_as_corners([
                light.get_center(), ball.get_center(), point
            ])
            beam.set_stroke(YELLOW, 5)
            beam.set_flat_stroke(False)
            beam.insert_n_curves(100)
            beams.add(beam)

        frame.reorient(-36, 70, 0) 
        frame.clear_updaters()
        frame.add_updater(lambda m, dt: m.increment_theta(dt * 3 * DEGREES))
        for beam in beams:
            self.play(
                VShowPassingFlash(
                    beam,
                    time_width=0.3,
                    run_time=1.5
                )
            )

    def get_plane_and_axes(self):
        axes = ThreeDAxes(axis_config=dict(tick_size=0))
        axes.set_stroke(opacity=0.5)
        plane = NumberPlane(
            x_range=axes.x_range,
            y_range=axes.y_range,
            background_line_style=dict(
                stroke_color=GREY_B,
                stroke_width=1.0,
                stroke_opacity=0.5,
            )
        )
        plane.axes.set_opacity(0)
        return plane, axes
