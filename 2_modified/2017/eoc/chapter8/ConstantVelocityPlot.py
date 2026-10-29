# ==============================================================================
# Scene:      ConstantVelocityPlot
# Source:     videos/_2017/eoc/chapter8.py (lines 543-702)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl ConstantVelocityPlot.py ConstantVelocityPlot -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - NameError in the original: draw_curve unpacks `label` but writes `graph_label`
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

DISTANCE_COLOR = BLUE


TIME_COLOR = YELLOW


VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter8.py -----

def v_rate_func(t):
    return 4*t - 4*(t**2)


def v_func(t):
    return t*(8-t)


class PlotVelocity(GraphScene):
    CONFIG = {
        "x_min" : -1,
        "x_max" : 9,
        "x_axis_width" : 9,
        "x_tick_frequency" : 1,
        "x_labeled_nums" : list(range(1, 9)),
        "x_axis_label" : "$t$",
        "y_min" : 0,
        "y_max" : 25,
        "y_axis_height" : 6,
        "y_tick_frequency" : 5,
        "y_labeled_nums" : list(range(5, 30, 5)),
        "y_axis_label" : "Velocity in $\\frac{\\text{meters}}{\\text{second}}$",
        "num_graph_anchor_points" : 50,
    }
    def construct(self):
        self.setup_axes()
        self.add_speedometer()
        self.plot_points()
        self.draw_curve()

    def add_speedometer(self):
        speedometer = Speedometer()
        speedometer.next_to(self.y_axis_label_mob, RIGHT, LARGE_BUFF)
        speedometer.to_edge(UP)

        self.play(DrawBorderThenFill(
            speedometer, 
            lag_ratio = 0.5,
            rate_func=linear,
        ))

        self.speedometer = speedometer

    def plot_points(self):
        times = list(range(0, 9))
        points = [
            self.coords_to_point(t, v_func(t))
            for t in times
        ]
        dots = VGroup(*[Dot(p, radius = 0.07) for p in points])
        dots.set_color(VELOCITY_COLOR)

        pre_dots = VGroup()
        dot_intro_anims = []

        for time, dot in zip(times, dots):
            pre_dot = dot.copy()
            self.speedometer.move_needle_to_velocity(v_func(time))
            pre_dot.move_to(self.speedometer.get_needle_tip())
            pre_dot.set_fill(opacity = 0)
            pre_dots.add(pre_dot)
            dot_intro_anims += [
                ApplyMethod(
                    pre_dot.set_fill, YELLOW, 1,
                    run_time = 0.1,
                ),
                ReplacementTransform(
                    pre_dot, dot,
                    run_time = 0.9,
                )
            ]
        self.speedometer.move_needle_to_velocity(0)

        self.play(
            Succession(
                *dot_intro_anims, rate_func=linear
            ),
            ApplyMethod(
                self.speedometer.move_needle_to_velocity,
                v_func(4),
                rate_func = squish_rate_func(
                    lambda t : 1-v_rate_func(t),
                    0, 0.95,
                )
            ),
            run_time = 5
        )
        self.wait()

    def draw_curve(self):
        graph, label = self.get_v_graph_and_label()

        self.revert_to_original_skipping_status()
        self.play(ShowCreation(graph, run_time = 3))
        # CHANGE: NameError in the original: draw_curve unpacks `label` but writes `graph_label`
        self.play(Write(label))
        self.wait()

    ##

    def get_v_graph_and_label(self):
        graph = self.get_graph(
            v_func, 
            x_min = 0,
            x_max = 8,
            color = VELOCITY_COLOR
        )
        graph_label = OldTex("v(t)", "=t(8-t)")
        graph_label.set_color_by_tex("v(t)", VELOCITY_COLOR)
        graph_label.next_to(
            graph.point_from_proportion(7./8.),
            UP+RIGHT
        )
        self.v_graph = graph
        self.v_graph_label = graph_label
        return graph, graph_label


class ConstantVelocityPlot(PlotVelocity):
    CONFIG = {
        "x_axis_label" : "Time",
        "units_of_area_color" : BLUE_E,
    }
    def construct(self):
        self.setup_axes()
        self.x_axis_label_mob.shift(DOWN)
        self.draw_graph()
        self.show_product()
        self.comment_on_area_wierdness()
        self.note_units()

    def draw_graph(self):
        graph = self.get_graph(
            lambda t : 10,
            x_min = 0, 
            x_max = 8,
            color = VELOCITY_COLOR
        )

        self.play(ShowCreation(graph, rate_func=linear, run_time = 3))
        self.wait()

        self.graph = graph

    def show_product(self):
        rect = Rectangle(
            stroke_width = 0,
            fill_color = DISTANCE_COLOR,
            fill_opacity = 0.5
        )
        rect.replace(
            VGroup(self.graph, VectorizedPoint(self.graph_origin)),
            stretch = True
        )

        right_brace = Brace(rect, RIGHT)
        top_brace = Brace(rect, UP)
        v_label = right_brace.get_text(
            "$10 \\frac{\\text{meters}}{\\text{second}}$",
        )
        v_label.set_color(VELOCITY_COLOR)
        t_label = top_brace.get_text(
            "8 seconds"
        )
        t_label.set_color(TIME_COLOR)

        s_label = OldTex("10", "\\times",  "8", "\\text{ meters}")
        s_label.set_color_by_tex("10", VELOCITY_COLOR)
        s_label.set_color_by_tex("8", TIME_COLOR)
        s_label.move_to(rect)

        self.play(
            GrowFromCenter(right_brace),
            Write(v_label),
        )
        self.play(
            GrowFromCenter(top_brace),
            Write(t_label),
        )
        self.play(
            FadeIn(rect),
            Write(s_label),
            Animation(self.graph)
        )
        self.wait(2)

        self.area_rect = rect
        self.s_label = s_label

    def comment_on_area_wierdness(self):
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)
        bubble = randy.get_bubble(
            "Distance \\\\ is area?",
            bubble_type = ThoughtBubble,
            height = 3,
            width = 4,
            fill_opacity = 1,
        )
        bubble.content.scale(0.8)
        bubble.content.shift(SMALL_BUFF*UP)
        VGroup(bubble[-1], bubble.content).shift(1.5*LEFT)

        self.play(FadeIn(randy))
        self.play(randy.change_mode, "pondering")
        self.play(
            self.area_rect.set_color, YELLOW,
            *list(map(Animation, self.get_mobjects())),
            rate_func = there_and_back
        )
        self.play(Blink(randy))
        self.play(
            randy.change_mode, "confused",
            randy.look_at, randy.bubble,
            ShowCreation(bubble), 
            Write(bubble.content),
        )
        self.wait()
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.change_mode, "pondering",
            FadeOut(bubble),
            FadeOut(bubble.content),
        )

        self.randy = randy

    def note_units(self):
        x_line, y_line  = lines = VGroup(*[
            axis.copy()
            for axis in (self.x_axis, self.y_axis)
        ])
        lines.set_color(TIME_COLOR)
        square = Square(
            stroke_color = BLACK,
            stroke_width = 1,
            fill_color = self.units_of_area_color,
            fill_opacity = 1,
        )
        square.replace(
            VGroup(*[
                VectorizedPoint(self.coords_to_point(i, i))
                for i in (0, 1)
            ]),
            stretch = True
        )
        units_of_area = VGroup(*[
            square.copy().move_to(
                self.coords_to_point(x, y),
                DOWN+LEFT
            )
            for x in range(8)
            for y in range(10)
        ])

        self.play(ShowCreation(x_line))
        self.play(Indicate(self.x_axis_label_mob))
        self.play(FadeOut(x_line))
        self.play(
            ShowCreation(y_line),
            self.randy.look_at, self.y_axis_label_mob
        )
        self.play(Indicate(self.y_axis_label_mob))
        self.play(FadeOut(y_line))

        for FadeClass in FadeIn, FadeOut:
            self.play(
                FadeClass(
                    units_of_area, 
                    lag_ratio = 0.5,
                    run_time = 3
                ),
                Animation(self.s_label),
                self.randy.look_at, self.area_rect
            )
        self.play(Blink(self.randy))
        self.wait()
