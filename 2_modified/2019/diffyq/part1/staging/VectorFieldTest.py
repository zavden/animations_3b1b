# ==============================================================================
# Scene:      VectorFieldTest
# Source:     videos/_2019/diffyq/part1/staging.py (lines 13-46)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl VectorFieldTest.py VectorFieldTest -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use the Cairo vector field as a group of arrows, with delta_x/delta_y and get_vector, instead of the current GL API.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import CairoVectorField as VectorField


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def pendulum_vector_field_func(point, mu=0.1, g=9.8, L=3):
    theta, omega = point[:2]
    return np.array([
        omega,
        -np.sqrt(g / L) * np.sin(theta) - mu * omega,
        0,
    ])



# ----- From _2019/diffyq/part1/staging.py -----

class VectorFieldTest(Scene):
    def construct(self):
        plane = NumberPlane(
            # axis_config={"unit_size": 2}
        )
        mu_tracker = ValueTracker(1)
        field = VectorField(
            lambda p: pendulum_vector_field_func(
                plane.point_to_coords(p),
                mu=mu_tracker.get_value()
            ),
            delta_x=0.5,
            delta_y=0.5,
            max_magnitude=6,
            opacity=0.5,
            # length_func=lambda norm: norm,
        )
        field.set_opacity(1)

        self.add(plane, field)
        return

        stream_lines = StreamLines(
            field.func,
            delta_x=0.5,
            delta_y=0.5,
        )
        animated_stream_lines = AnimatedStreamLines(
            stream_lines,
            line_anim_class=ShowPassingFlashWithThinningStrokeWidth,
        )

        self.add(plane, field, animated_stream_lines)
        self.wait(10)
