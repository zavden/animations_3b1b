# ==============================================================================
# Scene:      PureAirfoilFlowCopy
# Source:     videos/_2018/turbulence.py (lines 811-815)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/div_curl.py
#
# Run from this folder:
#     manimgl PureAirfoilFlowCopy.py PureAirfoilFlowCopy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2018/div_curl.py -----

# Helper functions
def joukowsky_map(z):
    if z == 0:
        return 0
    return z + fdiv(1, z)


def inverse_joukowsky_map(w):
    u = 1 if w.real >= 0 else -1
    return (w + u * np.sqrt(w**2 - 4)) / 2


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
        for vector in vector_field:
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
        for stream_line in stream_lines:
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


class PureAirfoilFlow(PureCylinderFlow):
    def modify_flow(self, mobject):
        vect = 0.1 * LEFT + 0.2 * UP
        mobject.scale(get_norm(vect - RIGHT))
        mobject.shift(vect)
        mobject.apply_complex_function(joukowsky_map)
        return mobject

    def modify_vector_field(self, vector_field):
        def func(z):
            w = complex(-0.1, 0.2)
            n = abs(w - 1)
            return joukowsky_map(inverse_joukowsky_map(z) - w / n)

        def new_vector_field_func(point):
            z = R3_to_complex(point)
            return complex_to_R3(derivative(func)(z).conjugate())

        vf = VectorField(new_vector_field_func, delta_y=0.33)
        Transform(vector_field, vf).update(1)
        vf.set_fill(opacity=0.5)



# ----- From _2018/turbulence.py -----

class PureAirfoilFlowCopy(PureAirfoilFlow):
    def modify_vector_field(self, vector_field):
        PureAirfoilFlow.modify_vector_field(self, vector_field)
        vector_field.set_fill(opacity=0.1)
        vector_field.set_stroke(opacity=0.1)
