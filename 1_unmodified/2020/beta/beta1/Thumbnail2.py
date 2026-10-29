# ==============================================================================
# Scene:      Thumbnail2
# Source:     videos/_2020/beta/beta1.py (lines 71-119)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl Thumbnail2.py Thumbnail2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import scipy.stats


# ----- From _2020/beta/helpers.py -----

def get_beta_dist_axes(y_max=20, y_unit=2, label_y=False, **kwargs):
    config = {
        "x_min": 0,
        "x_max": 1,
        "x_axis_config": {
            "unit_size": 0.1,
            "tick_frequency": 0.1,
            "include_tip": False,
        },
        "y_min": 0,
        "y_max": y_max,
        "y_axis_config": {
            "unit_size": 1,
            "tick_frequency": y_unit,
            "include_tip": False,
        },
    }
    result = Axes(**config)
    origin = result.c2p(0, 0)
    kw = {
        "about_point": origin,
        "stretch": True,
    }
    result.x_axis.set_width(11, **kw)
    result.y_axis.set_height(6, **kw)

    x_vals = np.arange(0, 1, 0.2) + 0.2
    result.x_axis.add_numbers(
        *x_vals,
        num_decimal_places=1
    )

    if label_y:
        result.y_axis.add_numbers(
            *np.arange(y_unit, y_max, y_unit)
        )
        label = OldTexText("Probability density")
        label.scale(0.5)
        label.next_to(result.y_axis.get_top(), UR, SMALL_BUFF)
        label.next_to(result.y_axis, UP, SMALL_BUFF)
        label.align_to(result.y_axis.numbers, LEFT)
        result.add(label)
        result.y_axis_label = label

    result.to_corner(DR, LARGE_BUFF)

    return result


def close_off_graph(axes, graph):
    x_max = axes.x_axis.p2n(graph.get_end())
    graph.add_line_to(axes.c2p(x_max, 0))
    graph.add_line_to(axes.c2p(0, 0))
    return graph


def get_beta_graph(axes, n_plus, n_minus, **kwargs):
    dist = scipy.stats.beta(n_plus + 1, n_minus + 1)
    graph = axes.get_graph(dist.pdf, **kwargs)
    close_off_graph(axes, graph)
    graph.set_stroke(BLUE, 2)
    graph.set_fill(BLUE_E, 1)
    return graph



# ----- From _2020/beta/beta1.py -----

class Thumbnail2(Scene):
    def construct(self):
        axes = self.get_axes()
        graph = get_beta_graph(axes, 2, 2)
        # sub_graph = axes.get_graph(
        #     lambda x: (1 - x) * graph.underlying_function(x)
        # )
        # sub_graph.add_line_to(axes.c2p(1, 0))
        # sub_graph.add_line_to(axes.c2p(0, 0))
        # sub_graph.set_stroke(YELLOW, 4)
        # sub_graph.set_fill(YELLOW_D, 1)

        new_graph = get_beta_graph(axes, 9, 2)
        new_graph.set_stroke(GREEN, 4)
        new_graph.set_fill(GREEN, 0.5)

        self.add(axes)
        self.add(graph)
        self.add(new_graph)

        arrow = Arrow(
            axes.input_to_graph_point(0.5, graph),
            axes.input_to_graph_point(0.8, new_graph),
            path_arc=-90 * DEGREES,
            buff=0.3
        )
        self.add(arrow)

        formula = OldTex(
            "P(H|D) = {P(H)P(D|H) \\over P(D)}",
            tex_to_color_map={
                "H": YELLOW,
                "D": GREEN,
            }
        )
        formula.next_to(axes.c2p(0, 3), RIGHT, LARGE_BUFF)
        formula.set_height(1.5)
        formula.to_edge(LEFT)
        formula.to_edge(UP, LARGE_BUFF)
        formula.add_to_back(BackgroundRectangle(formula[:4], buff=0.25))

        self.add(formula)

    def get_axes(self, y_max=3, y_height=4.5, y_unit=0.5):
        axes = get_beta_dist_axes(y_max=y_max, y_unit=y_unit)
        axes.y_axis.set_height(y_height, about_point=axes.c2p(0, 0))
        axes.to_edge(DOWN)
        axes.scale(0.9)
        return axes
