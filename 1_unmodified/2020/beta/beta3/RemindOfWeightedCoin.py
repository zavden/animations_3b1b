# ==============================================================================
# Scene:      RemindOfWeightedCoin
# Source:     videos/_2020/beta/beta3.py (lines 11-314)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl RemindOfWeightedCoin.py RemindOfWeightedCoin -w -m --fps 15
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


def reverse_smooth(t):
    return smooth(1 - t)


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

class RemindOfWeightedCoin(Scene):
    def construct(self):
        # Largely copied from beta2

        # Prob label
        p_label = get_prob_coin_label()
        p_label.set_height(0.7)
        p_label.to_edge(UP)

        rhs = p_label[-1]
        q_box = get_q_box(rhs)
        p_label.add(q_box)

        self.add(p_label)

        # Coin grid
        def get_random_coin_grid(p):
            bools = np.random.random(100) < p
            grid = get_coin_grid(bools)
            return grid

        grid = get_random_coin_grid(0.5)
        grid.next_to(p_label, DOWN, MED_LARGE_BUFF)

        self.play(LaggedStartMap(
            FadeIn, grid,
            lag_ratio=2 / len(grid),
            run_time=3,
        ))
        self.wait()

        # Label as h
        brace = Brace(q_box, DOWN, buff=SMALL_BUFF)
        h_label = OldTex("h")
        h_label.next_to(brace, DOWN)
        eq = OldTex("=")
        eq.next_to(h_label, RIGHT)
        h_decimal = DecimalNumber(0.5)
        h_decimal.next_to(eq, RIGHT)

        self.play(
            GrowFromCenter(brace),
            FadeIn(h_label, UP),
            grid.scale, 0.8, {"about_edge": DOWN},
        )
        self.wait()

        # Alternate weightings
        tail_grid = get_random_coin_grid(0)
        head_grid = get_random_coin_grid(1)
        grid70 = get_random_coin_grid(0.7)
        alt_grids = [tail_grid, head_grid, grid70]
        for ag in alt_grids:
            ag.replace(grid)

        for coins in [grid, *alt_grids]:
            for coin in coins:
                coin.generate_target()
                coin.target.rotate(90 * DEGREES, axis=UP)
                coin.target.set_opacity(0)

        def get_grid_swap_anims(g1, g2):
            return [
                LaggedStartMap(MoveToTarget, g1, lag_ratio=0.02, run_time=1.5, remover=True),
                LaggedStartMap(MoveToTarget, g2, lag_ratio=0.02, run_time=1.5, rate_func=reverse_smooth),
            ]

        self.play(
            FadeIn(eq),
            UpdateFromAlphaFunc(h_decimal, lambda m, a: m.set_opacity(a)),
            ChangeDecimalToValue(h_decimal, 0, run_time=2),
            *get_grid_swap_anims(grid, tail_grid)
        )
        self.wait()
        self.play(
            ChangeDecimalToValue(h_decimal, 1, run_time=1.5),
            *get_grid_swap_anims(tail_grid, head_grid)
        )
        self.wait()
        self.play(
            ChangeDecimalToValue(h_decimal, 0.7, run_time=1.5),
            *get_grid_swap_anims(head_grid, grid70)
        )
        self.wait()

        # Graph
        axes = scaled_pdf_axes()
        axes.to_edge(DOWN, buff=MED_SMALL_BUFF)
        axes.y_axis.numbers.set_opacity(0)
        axes.y_axis_label.set_opacity(0)

        h_lines = VGroup()
        for y in range(15):
            h_line = Line(axes.c2p(0, y), axes.c2p(1, y))
            h_lines.add(h_line)
        h_lines.set_stroke(WHITE, 0.5, opacity=0.5)
        axes.add(h_lines)

        x_axis_label = p_label[:4].copy()
        x_axis_label.set_height(0.4)
        x_axis_label.next_to(axes.c2p(1, 0), UR, buff=SMALL_BUFF)
        axes.x_axis.add(x_axis_label)

        n_heads_tracker = ValueTracker(3)
        n_tails_tracker = ValueTracker(3)

        def get_graph(axes=axes, nht=n_heads_tracker, ntt=n_tails_tracker):
            dist = scipy.stats.beta(nht.get_value() + 1, ntt.get_value() + 1)
            graph = axes.get_graph(dist.pdf, step_size=0.05)
            graph.set_stroke(BLUE, 3)
            graph.set_fill(BLUE_E, 1)
            return graph

        graph = always_redraw(get_graph)

        area_label = OldTexText("Area = 1")
        area_label.set_height(0.5)
        area_label.move_to(axes.c2p(0.5, 1))

        # pdf label
        pdf_label = OldTexText("probability ", "density ", "function")
        pdf_label.next_to(axes.input_to_graph_point(0.5, graph), UP)
        pdf_target_template = OldTexText("p", "d", "f")
        pdf_target_template.next_to(axes.input_to_graph_point(0.7, graph), UR)
        pdf_label.generate_target()
        for part, letter2 in zip(pdf_label.target, pdf_target_template):
            for letter1 in part:
                letter1.move_to(letter2)
            part[1:].set_opacity(0)

        # Add plot
        self.add(axes, *self.mobjects)
        self.play(
            FadeOut(eq),
            FadeOut(h_decimal),
            LaggedStartMap(MoveToTarget, grid70, run_time=1, remover=True),
            FadeIn(axes),
        )
        self.play(
            DrawBorderThenFill(graph),
            FadeIn(area_label, rate_func=squish_rate_func(smooth, 0.5, 1), run_time=2),
            Write(pdf_label, run_time=1),
        )
        self.wait()

        # Region
        lh_tracker = ValueTracker(0.7)
        rh_tracker = ValueTracker(0.7)

        def get_region(axes=axes, graph=graph, lh_tracker=lh_tracker, rh_tracker=rh_tracker):
            lh = lh_tracker.get_value()
            rh = rh_tracker.get_value()
            region = get_region_under_curve(axes, graph, lh, rh)
            region.set_fill(GREY, 0.85)
            region.set_stroke(YELLOW, 1)
            return region

        region = always_redraw(get_region)

        region_area_label = DecimalNumber(num_decimal_places=3)
        region_area_label.next_to(axes.c2p(0.7, 0), UP, MED_LARGE_BUFF)

        def update_ra_label(label, nht=n_heads_tracker, ntt=n_tails_tracker, lht=lh_tracker, rht=rh_tracker):
            dist = scipy.stats.beta(nht.get_value() + 1, ntt.get_value() + 1)
            area = dist.cdf(rht.get_value()) - dist.cdf(lht.get_value())
            label.set_value(area)

        region_area_label.add_updater(update_ra_label)

        range_label = VGroup(
            OldTex("0.6 \\le"),
            p_label[:4].copy(),
            OldTex("\\le 0.8"),
        )
        for mob in range_label:
            mob.set_height(0.4)
        range_label.arrange(RIGHT, buff=SMALL_BUFF)
        pp_label = VGroup(
            OldTex("P("),
            range_label,
            OldTex(")"),
        )
        for mob in pp_label[::2]:
            mob.set_height(0.7)
            mob.set_color(YELLOW)
        pp_label.arrange(RIGHT, buff=SMALL_BUFF)
        pp_label.move_to(axes.c2p(0.3, 3))

        self.play(
            FadeIn(pp_label[::2]),
            MoveToTarget(pdf_label),
            FadeOut(area_label),
        )
        self.wait()
        self.play(TransformFromCopy(p_label[:4], range_label[1]))
        self.wait()
        self.play(TransformFromCopy(axes.x_axis.numbers[2], range_label[0]))
        self.play(TransformFromCopy(axes.x_axis.numbers[3], range_label[2]))
        self.wait()

        self.add(region)
        self.play(
            lh_tracker.set_value, 0.6,
            rh_tracker.set_value, 0.8,
            UpdateFromAlphaFunc(
                region_area_label,
                lambda m, a: m.set_opacity(a),
                rate_func=squish_rate_func(smooth, 0.25, 1)
            ),
            run_time=3,
        )
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
        coins.next_to(h_label, DOWN, buff=MED_LARGE_BUFF)

        heads = [c for c in coins if c.symbol == "H"]
        numbers = VGroup(*[
            Integer(i + 1).set_height(0.2).next_to(coin, DOWN, SMALL_BUFF)
            for i, coin in enumerate(heads)
        ])

        for coin in coins:
            coin.save_state()
            coin.rotate(90 * DEGREES, UP)
            coin.set_opacity(0)

        pp_label.generate_target()
        pp_label.target.set_height(0.5)
        pp_label.target.next_to(axes.c2p(0, 2), RIGHT, MED_LARGE_BUFF)

        self.play(
            LaggedStartMap(Restore, coins),
            MoveToTarget(pp_label),
            run_time=1,
        )
        self.play(ShowIncreasingSubsets(numbers))
        self.wait()

        # Move plot
        self.play(
            n_heads_tracker.set_value, 7,
            n_tails_tracker.set_value, 3,
            FadeOut(pdf_label, rate_func=squish_rate_func(smooth, 0, 0.5)),
            run_time=2
        )
        self.wait()

        # How does the answer change with more data
        new_bools = [True] * 63 + [False] * 27
        random.shuffle(new_bools)
        bools = [c.symbol == "H" for c in coins] + new_bools
        grid = get_coin_grid(bools)
        grid.set_height(3.5)
        grid.next_to(axes.c2p(0, 3), RIGHT, MED_LARGE_BUFF)

        self.play(
            FadeOut(numbers),
            ReplacementTransform(coins, grid[:10]),
        )
        self.play(
            FadeIn(grid[10:], lag_ratio=0.1, rate_func=linear),
            pp_label.next_to, grid, DOWN,
        )
        self.wait()
        self.add(graph, region, region_area_label, p_label, q_box, brace, h_label)
        self.play(
            n_heads_tracker.set_value, 70,
            n_tails_tracker.set_value, 30,
        )
        self.wait()
        origin = axes.c2p(0, 0)
        self.play(
            axes.y_axis.stretch, 0.5, 1, {"about_point": origin},
            h_lines.stretch, 0.5, 1, {"about_point": origin},
        )
        self.wait()

        # Shift the shape around
        pairs = [
            (70 * 3, 30 * 3),
            (35, 15),
            (35 + 20, 15 + 20),
            (7, 3),
            (70, 30),
        ]
        for nh, nt in pairs:
            self.play(
                n_heads_tracker.set_value, nh,
                n_tails_tracker.set_value, nt,
                run_time=2,
            )
            self.wait()

        # End
        self.embed()
