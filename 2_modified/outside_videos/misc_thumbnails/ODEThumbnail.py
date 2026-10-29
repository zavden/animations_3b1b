# ==============================================================================
# Scene:      ODEThumbnail
# Source:     videos/outside_videos/misc_thumbnails.py (lines 212-252)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ODEThumbnail.py ODEThumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Current VectorField: func vectorized over an (N, 2) array, density instead of step_multiple and max_vect_len instead of length_func
# ==============================================================================

from manim_imports_ext import *

def pendulum_vector_field_func(theta, omega, mu=0.3, g=9.8, L=3):
    return [omega, -np.sqrt(g / L) * np.sin(theta) - mu * omega]


class ODEThumbnail(Scene):
    def construct(self):
        plane = NumberPlane()
        # CHANGE: current VectorField: func vectorized over an (N, 2) array, density instead of step_multiple and max_vect_len instead of length_func
        field = VectorField(
            lambda coords: np.array(pendulum_vector_field_func(coords[:, 0], coords[:, 1])).T,
            plane,
            density=2.0,
            magnitude_range=(0, 5),
            max_vect_len=0.35,
        )
        field.set_opacity(0.75)

        # self.add(plane)
        # self.add(field)
        # return

        # Solution curve

        dt = 0.1
        t = 0
        total_time = 50

        def func(point):
            return plane.c2p(*pendulum_vector_field_func(*plane.p2c(point)))

        points = [plane.c2p(-4 * TAU / 4, 4.0)]
        while t < total_time:
            t += dt
            points.append(points[-1] + dt * func(points[-1]))

        line = VMobject()
        line.set_points_smoothly(points)
        line.set_stroke([WHITE, WHITE, BLACK], width=[5, 1])
        # line.set_stroke((BLUE_C, BLUE_E), width=(10, 1))

        line_fuzz = VGroup()
        N = 50
        for width in np.linspace(50, 0, N):
            line_fuzz.add(line.copy().set_stroke(BLACK, width=width, opacity=2 / N))

        self.add(line_fuzz)
        self.add(line)
