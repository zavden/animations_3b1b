# ==============================================================================
# Scene:      WeightedCoin
# Source:     videos/_2020/beta/beta2.py (lines 11-281)
# Category:   2 · Renders with modifications
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl WeightedCoin.py WeightedCoin -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - OldTex does not accept buff (a nonexistent kwarg before too: it ignored it); it is removed
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


def get_prob_coin_label(symbol="H", color=None, p=0.5, num_decimal_places=2):
    label = OldTex("P", "(", "00", ")", "=",)
    coin = get_coin(symbol, color)
    template = label.get_part_by_tex("00")
    coin.replace(template)
    label.replace_submobject(label.index_of_part(template), coin)
    rhs = DecimalNumber(p, num_decimal_places=num_decimal_places)
    rhs.next_to(label, RIGHT, buff=MED_SMALL_BUFF)
    label.add(rhs)
    return label


def get_q_box(mob):
    box = SurroundingRectangle(mob)
    box.set_stroke(WHITE, 1)
    box.set_fill(GREY_E, 1)
    q_marks = OldTex("???")
    max_width = 0.8 * box.get_width()
    max_height = 0.8 * box.get_height()

    if q_marks.get_width() > max_width:
        q_marks.set_width(max_width)

    if q_marks.get_height() > max_height:
        q_marks.set_height(max_height)

    q_marks.move_to(box)
    box.add(q_marks)
    return box


def get_coin_grid(bools, height=6):
    coins = VGroup(*[
        get_coin("H" if heads else "T")
        for heads in bools
    ])
    coins.arrange_in_grid()
    coins.set_height(height)
    return coins


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



# ----- From _2020/beta/beta2.py -----

class WeightedCoin(Scene):
    def construct(self):
        # Coin grid
        bools = 50 * [True] + 50 * [False]
        random.shuffle(bools)
        grid = get_coin_grid(bools)

        sorted_grid = VGroup(*grid)
        sorted_grid.submobjects.sort(key=lambda m: m.symbol)

        # Prob label
        p_label = get_prob_coin_label()
        p_label.set_height(0.7)
        p_label.to_edge(UP)

        rhs = p_label[-1]
        rhs_box = SurroundingRectangle(rhs, color=RED)
        rhs_label = OldTexText("Not necessarily")
        rhs_label.next_to(rhs_box, DOWN, LARGE_BUFF)
        rhs_label.to_edge(RIGHT)
        rhs_label.match_color(rhs_box)

        rhs_arrow = Arrow(
            rhs_label.get_top(),
            rhs_box.get_right(),
            buff=SMALL_BUFF,
            path_arc=60 * DEGREES,
            color=rhs_box.get_color()
        )

        # Introduce coin
        self.play(FadeIn(
            grid,
            run_time=2,
            rate_func=linear,
            lag_ratio=3 / len(grid),
        ))
        self.wait()
        self.play(
            grid.set_height, 5,
            grid.to_edge, DOWN,
            FadeInFromDown(p_label)
        )

        for coin in grid:
            coin.generate_target()
        sorted_coins = list(grid)
        sorted_coins.sort(key=lambda m: m.symbol)
        for c1, c2 in zip(sorted_coins, grid):
            c1.target.move_to(c2)

        self.play(
            FadeIn(rhs_label, lag_ratio=0.1),
            ShowCreation(rhs_arrow),
            ShowCreation(rhs_box),
            LaggedStartMap(
                MoveToTarget, grid,
                path_arc=30 * DEGREES,
                lag_ratio=0.01,
            ),
        )

        # Alternate weightings
        old_grid = VGroup(*sorted_coins)
        rhs_junk_on_screen = True
        for value in [0.2, 0.9, 0.0, 0.31]:
            n = int(100 * value)
            new_grid = get_coin_grid([True] * n + [False] * (100 - n))
            new_grid.replace(grid)

            anims = []
            if rhs_junk_on_screen:
                anims += [
                    FadeOut(rhs_box),
                    FadeOut(rhs_label),
                    FadeOut(rhs_arrow),
                ]
                rhs_junk_on_screen = False

            self.wait()
            self.play(
                FadeOut(
                    old_grid,
                    0.1 * DOWN,
                    lag_ratio=0.01,
                    run_time=1.5
                ),
                FadeIn(new_grid, lag_ratio=0.01, run_time=1.5),
                ChangeDecimalToValue(rhs, value),
                *anims,
            )
            old_grid = new_grid

        long_rhs = DecimalNumber(
            0.31415926,
            num_decimal_places=8,
            show_ellipsis=True,
        )
        long_rhs.match_height(rhs)
        long_rhs.move_to(rhs, DL)

        self.play(ShowIncreasingSubsets(long_rhs, rate_func=linear))
        self.wait()

        # You just don't know
        box = get_q_box(rhs)

        self.remove(rhs)
        self.play(
            FadeOut(old_grid, lag_ratio=0.1),
            FadeOut(long_rhs, 0.1 * RIGHT, lag_ratio=0.1),
            Write(box),
        )
        p_label.add(box)
        self.wait()

        # 7/10 heads
        bools = [True] * 7 + [False] * 3
        random.shuffle(bools)
        coins = VGroup(*[
            get_coin("H" if heads else "T")
            for heads in bools
        ])
        coins.arrange(RIGHT)
        coins.set_height(0.7)
        coins.next_to(p_label, DOWN, buff=LARGE_BUFF)

        heads_arrows = VGroup(*[
            Vector(
                0.5 * UP,
                max_stroke_width_to_length_ratio=15,
                max_tip_length_to_length_ratio=0.4,
            ).next_to(coin, DOWN)
            for coin in coins
            if coin.symbol == "H"
        ])
        numbers = VGroup(*[
            Integer(i + 1).next_to(arrow, DOWN, SMALL_BUFF)
            for i, arrow in enumerate(heads_arrows)
        ])

        for coin in coins:
            coin.save_state()
            coin.stretch(0, 0)
            coin.set_opacity(0)

        self.play(LaggedStartMap(Restore, coins), run_time=1)
        self.play(
            ShowIncreasingSubsets(heads_arrows),
            ShowIncreasingSubsets(numbers),
            rate_func=linear,
        )
        self.wait()

        # Plot
        axes = scaled_pdf_axes()
        axes.to_edge(DOWN, buff=MED_SMALL_BUFF)
        axes.y_axis.numbers.set_opacity(0)
        axes.y_axis_label.set_opacity(0)

        x_axis_label = p_label[:4].copy()
        x_axis_label.set_height(0.4)
        x_axis_label.next_to(axes.c2p(1, 0), UR, buff=SMALL_BUFF)
        axes.x_axis.add(x_axis_label)

        n_heads = 7
        n_tails = 3
        graph = get_beta_graph(axes, n_heads, n_tails)
        dist = scipy.stats.beta(n_heads + 1, n_tails + 1)
        true_graph = axes.get_graph(dist.pdf)

        v_line = Line(
            axes.c2p(0.7, 0),
            axes.input_to_graph_point(0.7, true_graph),
        )
        v_line.set_stroke(YELLOW, 4)

        region = get_region_under_curve(axes, true_graph, 0.6, 0.8)
        region.set_fill(GREY, 0.85)
        region.set_stroke(YELLOW, 1)

        eq_label = VGroup(
            p_label[:4].copy(),
            OldTex("= 0.7"),
        )
        for mob in eq_label:
            mob.set_height(0.4)
        eq_label.arrange(RIGHT, buff=SMALL_BUFF)
        pp_label = VGroup(
            OldTex("P("),
            eq_label,
            OldTex(")"),
        )
        for mob in pp_label[::2]:
            mob.set_height(0.7)
            mob.set_color(YELLOW)
        pp_label.arrange(RIGHT, buff=SMALL_BUFF)
        pp_label.move_to(axes.c2p(0.3, 3))

        self.play(
            FadeOut(heads_arrows),
            FadeOut(numbers),
            Write(axes),
            DrawBorderThenFill(graph),
        )
        self.play(
            FadeIn(pp_label[::2]),
            ShowCreation(v_line),
        )
        self.wait()
        self.play(TransformFromCopy(p_label[:4], eq_label[0]))
        self.play(
            GrowFromPoint(eq_label[1], v_line.get_center())
        )
        self.wait()

        # Look confused
        randy = Randolph()
        randy.set_height(1.5)
        randy.next_to(axes.c2p(0, 0), UR, MED_LARGE_BUFF)

        self.play(FadeIn(randy))
        self.play(randy.change, "confused", pp_label.get_top())
        self.play(Blink(randy))
        self.wait()
        self.play(FadeOut(randy))

        # Remind what the title is
        title = OldTexText(
            "Probabilities", "of", "Probabilities"
        )
        title.arrange(DOWN, aligned_edge=LEFT)
        title.next_to(axes.c2p(0, 0), UR, buff=MED_LARGE_BUFF)
        title.align_to(pp_label, LEFT)

        self.play(ShowIncreasingSubsets(title, rate_func=linear))
        self.wait()
        self.play(FadeOut(title))

        # Continuous values
        v_line.tracker = ValueTracker(0.7)
        v_line.axes = axes
        v_line.graph = true_graph
        v_line.add_updater(
            lambda m: m.put_start_and_end_on(
                m.axes.c2p(m.tracker.get_value(), 0),
                m.axes.input_to_graph_point(m.tracker.get_value(), m.graph),
            )
        )

        for value in [0.4, 0.9, 0.7]:
            self.play(
                v_line.tracker.set_value, value,
                run_time=3,
            )

        # Label h
        brace = Brace(rhs_box, DOWN, buff=SMALL_BUFF)
        # CHANGE: OldTex does not accept buff (a nonexistent kwarg before too: it ignored it); it is removed
        h_label = OldTex("h")
        h_label.set_color(YELLOW)
        h_label.next_to(brace, DOWN)

        self.play(
            LaggedStartMap(FadeOutAndShift, coins, lambda m: (m, DOWN)),
            GrowFromCenter(brace),
            Write(h_label),
        )
        self.wait()

        # End
        self.embed()
