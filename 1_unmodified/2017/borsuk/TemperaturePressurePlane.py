# ==============================================================================
# Scene:      TemperaturePressurePlane
# Source:     videos/_2017/borsuk.py (lines 639-693)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TemperaturePressurePlane.py TemperaturePressurePlane -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TemperaturePressurePlane(GraphScene):
    CONFIG = {
        "x_labeled_nums" : [],
        "y_labeled_nums" : [],
        "x_axis_label" : "Temperature",
        "y_axis_label" : "Pressure",
        "graph_origin" : 2.5*DOWN + 2*LEFT,
        "corner_square_width" : 4,
        "example_point_coords" : (2, 5),
    }
    def construct(self):
        self.setup_axes()
        self.draw_arrow()
        self.add_example_coordinates()
        self.wander_continuously()

    def draw_arrow(self):
        square = Square(
            side_length = self.corner_square_width,
            stroke_color = WHITE,
            stroke_width = 0,
        )
        square.to_corner(UP+LEFT, buff = 0)

        arrow = Arrow(
            square.get_right(), 
            self.coords_to_point(*self.example_point_coords)
        )

        self.play(ShowCreation(arrow))

    def add_example_coordinates(self):
        dot = Dot(self.coords_to_point(*self.example_point_coords))
        dot.set_color(YELLOW)
        tex = OldTex("(25^\\circ\\text{C}, 101 \\text{ kPa})")
        tex.next_to(dot, UP+RIGHT, buff = SMALL_BUFF)

        self.play(ShowCreation(dot))
        self.play(Write(tex))
        self.wait()
        self.play(FadeOut(tex))

    def wander_continuously(self):
        path = VMobject().set_points_smoothly([
            ORIGIN, 2*UP+RIGHT, 2*DOWN+RIGHT,
            5*RIGHT, 4*RIGHT+UP, 3*RIGHT+2*DOWN,
            DOWN+LEFT, 2*RIGHT
        ])
        point = self.coords_to_point(*self.example_point_coords)
        path.shift(point)

        path.set_color(GREEN)

        self.play(ShowCreation(path, run_time = 10, rate_func=linear))
        self.wait()
