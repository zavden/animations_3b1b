# ==============================================================================
# Scene:      PreviewBeta
# Source:     videos/_2020/beta/beta1.py (lines 2182-2237)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl PreviewBeta.py PreviewBeta -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import scipy.stats


# ----- From _2020/beta/helpers.py -----

CMARK_TEX = "\\text{\\ding{51}}"


XMARK_TEX = "\\text{\\ding{55}}"


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


def get_beta_label(n_plus, n_minus, point=ORIGIN):
    template = OldTexText("Beta(", "00", ",", "00", ")")
    template.scale(1.5)
    a_label = Integer(n_plus + 1)
    a_label.set_color(GREEN)
    b_label = Integer(n_minus + 1)
    b_label.set_color(RED)

    for i, label in (1, a_label), (3, b_label):
        label.match_height(template[i])
        label.move_to(template[i], DOWN)
        template.replace_submobject(i, label)
    template.save_state()
    template.arrange(RIGHT, buff=0.15)
    for t1, t2 in zip(template, template.saved_state):
        t1.align_to(t2, DOWN)

    return template


def get_plusses_and_minuses(n_rows=15, n_cols=20, p=0.95):
    result = VGroup()
    for x in range(n_rows * n_cols):
        if random.random() < p:
            mob = OldTex(CMARK_TEX)
            mob.set_color(GREEN)
            mob.is_plus = True
        else:
            mob = OldTex(XMARK_TEX)
            mob.set_color(RED)
            mob.is_plus = False
        mob.set_width(1)
        result.add(mob)

    result.arrange_in_grid(n_rows, n_cols)
    result.set_width(5.5)
    return result



# ----- From _2020/beta/beta1.py -----

class PreviewBeta(Scene):
    def construct(self):
        axes = get_beta_dist_axes(label_y=True)
        axes.y_axis.remove(axes.y_axis.numbers)
        marks = get_plusses_and_minuses(p=0.75)
        marks.next_to(axes.y_axis.get_top(), DR, buff=0.75)

        beta_label = get_beta_label(0, 0)
        beta_label.next_to(marks, UR, buff=LARGE_BUFF)
        beta_label.to_edge(UP)
        bl_left = beta_label.get_left()

        beta_container = VGroup()
        graph_container = VGroup()
        n_graphs = 2
        for x in range(n_graphs):
            graph_container.add(VMobject())

        def get_counts(marks):
            is_plusses = [m.is_plus for m in marks]
            p = sum(is_plusses)
            n = len(is_plusses) - p
            return p, n

        def update_beta(container):
            counts = get_counts(marks)
            new_label = get_beta_label(*counts)
            new_label.move_to(bl_left, LEFT)
            container.set_submobjects([new_label])
            return container

        def update_graph(container):
            counts = get_counts(marks)
            new_graph = get_beta_graph(axes, *counts)
            new_graphs = [*container[1:], new_graph]
            for g, a in zip(new_graphs, np.linspace(0.2, 1, n_graphs)):
                g.set_opacity(a)

            container.set_submobjects(new_graphs)
            return container

        self.add(axes)
        self.play(
            ShowIncreasingSubsets(marks),
            UpdateFromFunc(
                beta_container,
                update_beta,
            ),
            UpdateFromFunc(
                graph_container,
                update_graph,
            ),
            run_time=15,
            rate_func=bezier([0, 0, 1, 1]),
        )
        self.wait()
