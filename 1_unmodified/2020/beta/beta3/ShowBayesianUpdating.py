# ==============================================================================
# Scene:      ShowBayesianUpdating
# Source:     videos/_2020/beta/beta3.py (lines 445-739)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl ShowBayesianUpdating.py ShowBayesianUpdating -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import scipy.stats


# ----- From _2020/beta/helpers.py -----

COIN_COLOR_MAP = {
    "H": BLUE_E,
    "T": RED_E,
}


# Coins
def get_coin(symbol, color=None):
    if color is None:
        color = COIN_COLOR_MAP.get(symbol, GREY_E)
    coin = VGroup()
    circ = Circle()
    circ.set_fill(color, 1)
    circ.set_stroke(WHITE, 1)
    circ.set_height(1)
    label = OldTexText(symbol)
    label.set_height(0.5 * circ.get_height())
    label.move_to(circ)
    coin.add(circ, label)
    coin.symbol = symbol
    return coin


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


def scaled_pdf_axes(scale_factor=3.5):
    axes = get_beta_dist_axes(
        label_y=True,
        y_unit=1,
    )
    axes.y_axis.numbers.set_submobjects([
        *axes.y_axis.numbers[:5],
        *axes.y_axis.numbers[4::5]
    ])
    sf = scale_factor
    axes.y_axis.stretch(sf, 1, about_point=axes.c2p(0, 0))
    for number in axes.y_axis.numbers:
        number.stretch(1 / sf, 1)
    axes.y_axis_label.to_edge(LEFT)
    axes.y_axis_label.add_background_rectangle(opacity=1)
    axes.set_stroke(background=True)
    return axes


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


def get_region_under_curve(axes, graph, min_x, max_x):
    props = [
        binary_search(
            function=lambda a: axes.x_axis.p2n(graph.pfp(a)),
            target=x,
            lower_bound=axes.x_min,
            upper_bound=axes.x_max,
        )
        for x in [min_x, max_x]
    ]
    region = graph.copy()
    region.pointwise_become_partial(graph, *props)
    region.add_line_to(axes.c2p(max_x, 0))
    region.add_line_to(axes.c2p(min_x, 0))
    region.add_line_to(region.get_start())

    region.set_stroke(GREEN, 2)
    region.set_fill(GREEN, 0.5)

    region.axes = axes
    region.graph = graph
    region.min_x = min_x
    region.max_x = max_x

    return region



# ----- From _2020/beta/beta3.py -----

# From version 1
class ShowBayesianUpdating(Scene):
    CONFIG = {
        "true_p": 0.72,
        "random_seed": 4,
        "initial_axis_scale_factor": 3.5
    }

    def construct(self):
        # Axes
        axes = scaled_pdf_axes(self.initial_axis_scale_factor)
        self.add(axes)

        # Graph
        n_heads = 0
        n_tails = 0
        graph = get_beta_graph(axes, n_heads, n_tails)
        self.add(graph)

        # Get coins
        true_p = self.true_p
        bool_values = np.random.random(100) < true_p
        bool_values[1] = True
        coins = self.get_coins(bool_values)
        coins.next_to(axes.y_axis, RIGHT, MED_LARGE_BUFF)
        coins.to_edge(UP, LARGE_BUFF)

        # Probability label
        p_label, prob, prob_box = self.get_probability_label()
        self.add(p_label)
        self.add(prob_box)

        # Slow animations
        def head_likelihood(x):
            return x

        def tail_likelihood(x):
            return 1 - x

        n_previews = 10
        n_slow_previews = 5
        for x in range(n_previews):
            coin = coins[x]
            is_heads = bool_values[x]

            new_data_label = OldTexText("New data")
            new_data_label.set_height(0.3)
            arrow = Vector(0.5 * UP)
            arrow.next_to(coin, DOWN, SMALL_BUFF)
            new_data_label.next_to(arrow, DOWN, SMALL_BUFF)
            new_data_label.shift(MED_SMALL_BUFF * RIGHT)

            if is_heads:
                line = axes.get_graph(lambda x: x)
                label = OldTex("\\text{Scale by } x")
                likelihood = head_likelihood
                n_heads += 1
            else:
                line = axes.get_graph(lambda x: 1 - x)
                label = OldTex("\\text{Scale by } (1 - x)")
                likelihood = tail_likelihood
                n_tails += 1
            label.next_to(graph, UP)
            label.set_stroke(BLACK, 3, background=True)
            line.set_stroke(YELLOW, 3)

            graph_copy = graph.copy()
            scaled_graph = graph.copy()
            scaled_graph.apply_function(
                lambda p: axes.c2p(
                    axes.x_axis.p2n(p),
                    axes.y_axis.p2n(p) * likelihood(axes.x_axis.p2n(p))
                )
            )
            scaled_graph.set_color(GREEN)

            renorm_label = OldTexText("Renormalize")
            renorm_label.move_to(label)

            new_graph = get_beta_graph(axes, n_heads, n_tails)

            renormalized_graph = scaled_graph.copy()
            renormalized_graph.match_style(graph)
            renormalized_graph.match_height(new_graph, stretch=True, about_edge=DOWN)

            if x < n_slow_previews:
                self.play(
                    FadeInFromDown(coin),
                    FadeIn(new_data_label),
                    GrowArrow(arrow),
                )
                self.play(
                    FadeOut(new_data_label),
                    FadeOut(arrow),
                    ShowCreation(line),
                    FadeIn(label),
                )
                self.add(graph_copy, line, label)
                self.play(Transform(graph_copy, scaled_graph))
                self.play(
                    FadeOut(line),
                    FadeOut(label),
                    FadeIn(renorm_label),
                )
                self.play(
                    Transform(graph_copy, renormalized_graph),
                    FadeOut(graph),
                )
                self.play(FadeOut(renorm_label))
            else:
                self.add(coin)
                graph_copy.become(scaled_graph)
                self.add(graph_copy)
                self.play(
                    Transform(graph_copy, renormalized_graph),
                    FadeOut(graph),
                )
            graph = new_graph
            self.remove(graph_copy)
            self.add(new_graph)

        # Rescale y axis
        axes.save_state()
        sf = self.initial_axis_scale_factor
        axes.y_axis.stretch(1 / sf, 1, about_point=axes.c2p(0, 0))
        for number in axes.y_axis.numbers:
            number.stretch(sf, 1)
        axes.y_axis.numbers[:4].set_opacity(0)

        self.play(
            Restore(axes, rate_func=lambda t: smooth(1 - t)),
            graph.stretch, 1 / sf, 1, {"about_edge": DOWN},
            run_time=2,
        )

        # Fast animations
        for x in range(n_previews, len(coins)):
            coin = coins[x]
            is_heads = bool_values[x]

            if is_heads:
                n_heads += 1
            else:
                n_tails += 1
            new_graph = get_beta_graph(axes, n_heads, n_tails)

            self.add(coins[:x + 1])
            self.add(new_graph)
            self.remove(graph)
            self.wait(0.25)
            # self.play(
            #     FadeIn(new_graph),
            #     run_time=0.25,
            # )
            # self.play(
            #     FadeOut(graph),
            #     run_time=0.25,
            # )
            graph = new_graph

        # Show confidence interval
        dist = scipy.stats.beta(n_heads + 1, n_tails + 1)
        v_lines = VGroup()
        labels = VGroup()
        x_bounds = dist.interval(0.95)
        for x in x_bounds:
            line = DashedLine(
                axes.c2p(x, 0),
                axes.c2p(x, 12),
            )
            line.set_color(YELLOW)
            v_lines.add(line)
            label = DecimalNumber(x)
            label.set_height(0.25)
            label.next_to(line, UP)
            label.match_color(line)
            labels.add(label)

        true_graph = axes.get_graph(dist.pdf)
        region = get_region_under_curve(axes, true_graph, *x_bounds)
        region.set_fill(GREY_BROWN, 0.85)
        region.set_stroke(YELLOW, 1)

        label95 = OldTex("95\\%")
        fix_percent(label95.family_members_with_points()[-1])
        label95.move_to(region, DOWN)
        label95.shift(0.5 * UP)

        self.play(*map(ShowCreation, v_lines))
        self.play(
            FadeIn(region),
            Write(label95)
        )
        self.wait()
        for label in labels:
            self.play(FadeInFromDown(label))
        self.wait()

        # Show true value
        self.wait()
        self.play(FadeOut(prob_box))
        self.play(ShowCreationThenFadeAround(prob))
        self.wait()

        # Much more data
        many_bools = np.hstack([
            bool_values,
            (np.random.random(1000) < true_p)
        ])
        N_tracker = ValueTracker(100)
        graph.N_tracker = N_tracker
        graph.bools = many_bools
        graph.axes = axes
        graph.v_lines = v_lines
        graph.labels = labels
        graph.region = region
        graph.label95 = label95

        label95.width_ratio = label95.get_width() / region.get_width()

        def update_graph(graph):
            N = int(graph.N_tracker.get_value())
            nh = sum(graph.bools[:N])
            nt = len(graph.bools[:N]) - nh
            new_graph = get_beta_graph(graph.axes, nh, nt, step_size=0.05)
            graph.become(new_graph)

            dist = scipy.stats.beta(nh + 1, nt + 1)
            x_bounds = dist.interval(0.95)
            for x, line, label in zip(x_bounds, graph.v_lines, graph.labels):
                line.set_x(graph.axes.c2p(x, 0)[0])
                label.set_x(graph.axes.c2p(x, 0)[0])
                label.set_value(x)

            graph.labels[0].shift(MED_SMALL_BUFF * LEFT)
            graph.labels[1].shift(MED_SMALL_BUFF * RIGHT)

            new_simple_graph = graph.axes.get_graph(dist.pdf)
            new_region = get_region_under_curve(graph.axes, new_simple_graph, *x_bounds)
            new_region.match_style(graph.region)
            graph.region.become(new_region)

            graph.label95.set_width(graph.label95.width_ratio * graph.region.get_width())
            graph.label95.match_x(graph.region)

        self.add(graph, region, label95, p_label)
        self.play(
            N_tracker.set_value, 1000,
            UpdateFromFunc(graph, update_graph),
            Animation(v_lines),
            Animation(labels),
            Animation(graph.region),
            Animation(graph.label95),
            run_time=5,
        )
        self.wait()

    #

    def get_coins(self, bool_values):
        coins = VGroup(*[
            get_coin("H" if heads else "T")
            for heads in bool_values
        ])
        coins.arrange_in_grid(n_rows=10, buff=MED_LARGE_BUFF)
        coins.set_height(5)
        return coins

    def get_probability_label(self):
        head = get_coin("H")
        p_label = OldTex(
            "P(00) = ",
            tex_to_color_map={"00": WHITE}
        )
        template = p_label.get_part_by_tex("00")
        head.replace(template)
        p_label.replace_submobject(
            p_label.index_of_part(template),
            head,
        )
        prob = DecimalNumber(self.true_p)
        prob.next_to(p_label, RIGHT)
        p_label.add(prob)
        p_label.set_height(0.75)
        p_label.to_corner(UR)

        prob_box = SurroundingRectangle(prob, buff=SMALL_BUFF)
        prob_box.set_fill(GREY_D, 1)
        prob_box.set_stroke(WHITE, 2)

        q_marks = OldTex("???")
        q_marks.move_to(prob_box)
        prob_box.add(q_marks)

        return p_label, prob, prob_box
