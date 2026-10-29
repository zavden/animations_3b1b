# ==============================================================================
# Scene:      GraphOfXCubed
# Source:     videos/_2017/eoc/chapter3.py (lines 1197-1277)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl GraphOfXCubed.py GraphOfXCubed -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter3.py -----

DERIVATIVE_COLOR = VELOCITY_COLOR


class GraphOfXCubed(GraphScene):
    CONFIG = {
        "x_min" : -6,
        "x_max" : 6,
        "x_axis_width" : FRAME_WIDTH,
        "x_labeled_nums" : list(range(-6, 7)),
        "y_min" : -35,
        "y_max" : 35,
        "y_axis_height" : FRAME_HEIGHT,
        "y_tick_frequency" : 5,
        "y_labeled_nums" : list(range(-30, 40, 10)),
        "graph_origin" : ORIGIN,
        "dx" : 0.2,
        "deriv_x_min" : -3,
        "deriv_x_max" : 3,
    }
    def construct(self):
        self.setup_axes(animate = False)
        graph = self.get_graph(lambda x : x**3)
        label = self.get_graph_label(
            graph, "f(x) = x^3",
            direction = LEFT,
        )


        deriv_graph, full_deriv_graph = [
            self.get_derivative_graph(
                graph,
                color = DERIVATIVE_COLOR,
                x_min = low_x,
                x_max = high_x,
            )
            for low_x, high_x in [
                (self.deriv_x_min, self.deriv_x_max),
                (self.x_min, self.x_max),
            ]
        ]
        deriv_label = self.get_graph_label(
            deriv_graph,
            "\\frac{df}{dx}(x) = 3x^2",
            x_val = -3, 
            direction = LEFT
        )
        deriv_label.shift(0.5*DOWN)

        ss_group = self.get_secant_slope_group(
            self.deriv_x_min, graph, 
            dx = self.dx,
            dx_line_color = WHITE,
            df_line_color = WHITE,
            secant_line_color = YELLOW,
        )

        self.play(ShowCreation(graph))
        self.play(Write(label, run_time = 1))
        self.wait()
        self.play(Write(deriv_label, run_time = 1))
        self.play(ShowCreation(ss_group, lag_ratio = 0))
        self.animate_secant_slope_group_change(
            ss_group,
            target_x = self.deriv_x_max,
            run_time = 10,
            added_anims = [
                ShowCreation(deriv_graph, run_time = 10)
            ]
        )
        self.play(FadeIn(full_deriv_graph))
        self.wait()
        for x_val in -2, -self.dx/2, 2:
            self.animate_secant_slope_group_change(
                ss_group,
                target_x = x_val,
                run_time = 2
            )
            if x_val != -self.dx/2:
                v_line = self.get_vertical_line_to_graph(
                    x_val, deriv_graph,
                    line_class = DashedLine
                )
                self.play(ShowCreation(v_line))
                self.play(FadeOut(v_line))
