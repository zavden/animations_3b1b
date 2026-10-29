# ==============================================================================
# Scene:      LookAtAllPossibleSuccessRates
# Source:     videos/_2020/beta/beta1.py (lines 1548-1677)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl LookAtAllPossibleSuccessRates.py LookAtAllPossibleSuccessRates -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import scipy.stats


# ----- From _2020/beta/helpers.py -----

def get_prob_positive_experience_label(include_equals=False,
                                       include_decimal=False,
                                       include_q_mark=False):
    label = OldTex(
        "P", "(", "00000", ")",
    )

    pe = OldTexText("Positive\\\\experience")
    pe.set_color(GREEN)
    pe.replace(label[2], dim_to_match=0)
    label.replace_submobject(2, pe)
    VGroup(label[1], label[3]).match_height(
        pe, stretch=True, about_edge=DOWN,
    )
    if include_equals:
        eq = OldTex("=").next_to(label, RIGHT)
        label.add(eq)
    if include_decimal:
        decimal = DecimalNumber(0.95)
        decimal.next_to(label, RIGHT)
        decimal.set_color(YELLOW)
        label.decimal = decimal
        label.add(decimal)
    if include_q_mark:
        q_mark = OldTex("?")
        q_mark.relative_mob = label[-1]
        q_mark.add_updater(
            lambda m: m.next_to(m.relative_mob, RIGHT, SMALL_BUFF)
        )
        label.add(q_mark)

    return label


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



# ----- From _2020/beta/beta1.py -----

class LookAtAllPossibleSuccessRates(Scene):
    def construct(self):
        axes = get_beta_dist_axes(y_max=6, y_unit=1)
        dist = scipy.stats.beta(10, 2)
        graph = axes.get_graph(dist.pdf)
        graph.set_stroke(BLUE, 3)
        flat_graph = graph.copy()
        flat_graph.get_points()[:, 1] = axes.c2p(0, 0)[1]
        flat_graph.set_stroke(YELLOW, 3)

        x_labels = axes.x_axis.numbers
        x_labels.set_opacity(0)

        sellers = VGroup(*[
            self.get_example_seller(label.get_value())
            for label in x_labels
        ])
        sellers.arrange(RIGHT, buff=LARGE_BUFF)
        sellers.set_width(FRAME_WIDTH - 1)
        sellers.to_edge(UP, buff=LARGE_BUFF)

        sellers.generate_target()
        for seller, label in zip(sellers.target, x_labels):
            seller.next_to(label, DOWN)
            seller[0].set_opacity(0)
            seller[1].set_opacity(0)
            seller[2].replace(label, dim_to_match=1)

        x_label = OldTexText("All possible success rates")
        x_label.next_to(axes.c2p(0.5, 0), UP)
        x_label.shift(2 * LEFT)

        y_axis_label = OldTexText(
            "A kind of probability\\\\",
            "of probabilities"
        )
        y_axis_label.scale(0.75)
        y_axis_label.next_to(axes.y_axis, RIGHT)
        y_axis_label.to_edge(UP)
        y_axis_label[1].set_color(YELLOW)

        graph_label = OldTexText(
            "Some notion of likelihood\\\\",
            "for each one"
        )
        graph_label[1].align_to(graph_label[0], LEFT)
        graph_label.next_to(graph.get_boundary_point(UP), UP)
        graph_label.shift(0.5 * DOWN)
        graph_label.to_edge(RIGHT)

        x_axis_line = Line(axes.c2p(0, 0), axes.c2p(1, 0))
        x_axis_line.set_stroke(YELLOW, 3)

        shuffled_sellers = VGroup(*sellers)
        shuffled_sellers.shuffle()
        self.play(GrowFromCenter(shuffled_sellers[0]))
        self.play(LaggedStartMap(
            FadeInFromPoint, shuffled_sellers[1:],
            lambda m: (m, sellers.get_center())
        ))
        self.wait()
        self.play(
            MoveToTarget(sellers),
            FadeIn(axes),
            run_time=2,
        )

        self.play(
            x_label.shift, 4 * RIGHT,
            UpdateFromAlphaFunc(
                x_label,
                lambda m, a: m.set_opacity(a),
                rate_func=there_and_back,
            ),
            ShowCreation(x_axis_line),
            run_time=3,
        )
        self.play(FadeOut(x_axis_line))
        self.wait()
        self.play(
            FadeInFromDown(graph_label),
            ReplacementTransform(flat_graph, graph),
        )
        self.wait()
        self.play(FadeInFromDown(y_axis_label))

        # Show probabilities
        x_tracker = ValueTracker(0.5)

        prob_label = get_prob_positive_experience_label(True, True, True)
        prob_label.next_to(axes.c2p(0, 2), RIGHT, MED_LARGE_BUFF)
        prob_label.decimal.tracker = x_tracker
        prob_label.decimal.add_updater(
            lambda m: m.set_value(m.tracker.get_value())
        )

        v_line = Line(DOWN, UP)
        v_line.set_stroke(YELLOW, 2)
        v_line.tracker = x_tracker
        v_line.graph = graph
        v_line.axes = axes
        v_line.add_updater(
            lambda m: m.put_start_and_end_on(
                m.axes.x_axis.n2p(m.tracker.get_value()),
                m.axes.input_to_graph_point(m.tracker.get_value(), m.graph),
            )
        )

        self.add(v_line)
        for x in [0.95, 0.8, 0.9]:
            self.play(
                x_tracker.set_value, x,
                run_time=4,
            )
        self.wait()

    def get_example_seller(self, success_rate):
        randy = Randolph(mode="coin_flip_1", height=1)
        label = OldTex("s = ")
        decimal = DecimalNumber(success_rate)
        decimal.match_height(label)
        decimal.next_to(label[-1], RIGHT)
        label.set_color(YELLOW)
        decimal.set_color(YELLOW)
        VGroup(label, decimal).next_to(randy, DOWN)
        result = VGroup(randy, label, decimal)
        result.randy = randy
        result.label = label
        result.decimal = decimal
        return result
