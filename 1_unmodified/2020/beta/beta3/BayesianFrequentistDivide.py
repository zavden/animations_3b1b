# ==============================================================================
# Scene:      BayesianFrequentistDivide
# Source:     videos/_2020/beta/beta3.py (lines 342-431)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl BayesianFrequentistDivide.py BayesianFrequentistDivide -w -m --fps 15
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



# ----- From _2020/beta/beta3.py -----

class BayesianFrequentistDivide(Scene):
    def construct(self):
        # Setup Bayesian vs. Frequentist divide
        b_label = OldTexText("Bayesian")
        f_label = OldTexText("Frequentist")
        labels = VGroup(b_label, f_label)
        for label, vect in zip(labels, [LEFT, RIGHT]):
            label.set_height(0.7)
            label.move_to(vect * FRAME_WIDTH / 4)
            label.to_edge(UP, buff=0.35)

        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH)
        h_line.next_to(labels, DOWN)
        v_line = Line(UP, DOWN)
        v_line.set_height(FRAME_HEIGHT)
        v_line.center()

        for label in labels:
            label.save_state()
            label.set_y(0)
            self.play(
                FadeIn(label, -normalize(label.get_center())),
            )
        self.wait()
        self.play(
            ShowCreation(VGroup(v_line, h_line)),
            *map(Restore, labels),
        )
        self.wait()

        # Overlay ShowBayesianUpdating in editing
        # Frequentist list (ignore?)
        kw = {
            "tex_to_color_map": {
                "$p$-value": YELLOW,
                "$H_0$": PINK,
                "$\\alpha$": BLUE,
            },
            "alignment": "",
        }
        freq_list = VGroup(
            OldTexText("1. State a null hypothesis $H_0$", **kw),
            OldTexText("2. Choose a test statistic,\\\\", "$\\qquad$ compute its value", **kw),
            OldTexText("3. Calculate a $p$-value", **kw),
            OldTexText("4. Choose a significance value $\\alpha$", **kw),
            OldTexText("5. Reject $H_0$ if $p$-value\\\\", "$\\qquad$ is less than $\\alpha$", **kw),
        )

        freq_list.set_width(0.5 * FRAME_WIDTH - 1)
        freq_list.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        freq_list.move_to(FRAME_WIDTH * RIGHT / 4)
        freq_list.to_edge(DOWN, buff=LARGE_BUFF)

        # Frequentist icon
        axes = get_beta_dist_axes(y_max=5, y_unit=1)
        axes.set_width(0.5 * FRAME_WIDTH - 1)
        axes.move_to(FRAME_WIDTH * RIGHT / 4 + DOWN)

        dist = scipy.stats.norm(0.5, 0.1)
        graph = axes.get_graph(dist.pdf)
        graphs = VGroup()
        for x_min, x_max in [(0, 0.3), (0.3, 0.7), (0.7, 1.0)]:
            graph = axes.get_graph(dist.pdf, x_min=x_min, x_max=x_max)
            graph.add_line_to(axes.c2p(x_max, 0))
            graph.add_line_to(axes.c2p(x_min, 0))
            graph.add_line_to(graph.get_start())
            graphs.add(graph)

        graphs.set_stroke(width=0)
        graphs.set_fill(RED, 1)
        graphs[1].set_fill(GREY_D, 1)

        H_words = VGroup(*[TexText("Reject\\\\$H_0$") for x in range(2)])
        for H_word, graph, vect in zip(H_words, graphs[::2], [RIGHT, LEFT]):
            H_word.next_to(graph, UP, MED_LARGE_BUFF)
            arrow = Arrow(
                H_word.get_bottom(),
                graph.get_center() + 0.75 * vect,
                buff=SMALL_BUFF
            )
            H_word.add(arrow)

        H_words.set_color(RED)
        self.add(H_words)

        self.add(axes)
        self.add(graphs)

        self.embed()
