# ==============================================================================
# Scene:      PureCylinderFlow
# Source:     videos/_2018/div_curl.py (lines 1978-2032)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PureCylinderFlow.py PureCylinderFlow -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - iterate over a copy: Cairo looped over split() (a new list) while GL iterates the live submobjects list, so adding/removing inside the loop skips or revisits items (the BackgroundRectangle loop never ends)
#   - iterate over a copy: Cairo looped over split() (a new list) while GL iterates the live submobjects list, so adding/removing inside the loop skips or revisits items (the BackgroundRectangle loop never ends)
# ==============================================================================

from manim_imports_ext import *

# Helper functions
def joukowsky_map(z):
    if z == 0:
        return 0
    return z + fdiv(1, z)


def derivative(func, dt=1e-7):
    return lambda z: (func(z + dt) - func(z)) / dt


def cylinder_flow_vector_field(point, R=1, U=1):
    z = R3_to_complex(point)
    # return complex_to_R3(1.0 / derivative(joukowsky_map)(z))
    return complex_to_R3(derivative(joukowsky_map)(z).conjugate())


class PureCylinderFlow(Scene):
    def construct(self):
        self.add_vector_field()
        self.begin_flow()
        self.add_circle()
        self.wait(5)

    def add_vector_field(self):
        vector_field = VectorField(
            cylinder_flow_vector_field,
        )
        # CHANGE: iterate over a copy: Cairo looped over split() (a new list) while GL iterates the live submobjects list, so adding/removing inside the loop skips or revisits items (the BackgroundRectangle loop never ends)
        for vector in list(vector_field):
            if get_norm(vector.get_start()) < 1:
                vector_field.remove(vector)
        vector_field.set_fill(opacity=0.75)
        self.modify_vector_field(vector_field)
        self.add_foreground_mobjects(vector_field)

    def begin_flow(self):
        stream_lines = StreamLines(
            cylinder_flow_vector_field,
            colors=[BLUE_E, BLUE_D, BLUE_C],
            start_points_generator_config={
                "delta_x": 0.125,
                "delta_y": 0.125,
            },
            virtual_time=5,
        )
        self.add(stream_lines)
        # CHANGE: iterate over a copy: Cairo looped over split() (a new list) while GL iterates the live submobjects list, so adding/removing inside the loop skips or revisits items (the BackgroundRectangle loop never ends)
        for stream_line in list(stream_lines):
            if get_norm(stream_line.get_points()[0]) < 1:
                stream_lines.remove(stream_line)

        self.modify_flow(stream_lines)

        stream_line_animation = AnimatedStreamLines(stream_lines)
        stream_line_animation.update(3)

        self.add(stream_line_animation)

    def add_circle(self):
        circle = Circle(
            radius=1,
            stroke_color=YELLOW,
            fill_color=BLACK,
            fill_opacity=1,
        )
        self.modify_flow(circle)
        self.add_foreground_mobjects(circle)

    def modify_flow(self, mobject):
        pass

    def modify_vector_field(self, vector_field):
        pass
