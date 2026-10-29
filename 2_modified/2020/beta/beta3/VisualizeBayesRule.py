# ==============================================================================
# Scene:      VisualizeBayesRule
# Source:     videos/_2020/beta/beta3.py (lines 846-1509)
# Category:   2 · Renders with modifications
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl VisualizeBayesRule.py VisualizeBayesRule -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - unlock_shader_data no longer exists in manimgl (there is no locked shader data); it is removed
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


def get_check_count_label(nc, nx, include_rect=True):
    result = VGroup(
        Integer(nc),
        OldTex(CMARK_TEX, color=GREEN),
        Integer(nx),
        OldTex(XMARK_TEX, color=RED),
    )
    result.arrange(RIGHT, buff=SMALL_BUFF)
    result[2:].shift(SMALL_BUFF * RIGHT)

    if include_rect:
        rect = SurroundingRectangle(result)
        rect.set_stroke(WHITE, 1)
        rect.set_fill(GREY_E, 1)
        result.add_to_back(rect)

    return result



# ----- From _2020/beta/beta3.py -----

class VisualizeBayesRule(Scene):
    def construct(self):
        self.show_continuum()
        self.show_arrows()
        self.show_discrete_probabilities()
        self.show_bayes_formula()
        self.parallel_universes()
        self.update_from_data()

    def show_continuum(self):
        axes = get_beta_dist_axes(y_max=1, y_unit=0.1)
        axes.y_axis.add_numbers(
            *np.arange(0.2, 1.2, 0.2),
            num_decimal_places=1,
        )

        p_label = OldTex(
            "P(s \\,|\\, \\text{data})",
            tex_to_color_map={
                "s": YELLOW,
                "\\text{data}": GREEN,
            }
        )
        p_label.scale(1.5)
        p_label.to_edge(UP, LARGE_BUFF)

        s_part = p_label.get_part_by_tex("s").copy()
        x_line = Line(axes.c2p(0, 0), axes.c2p(1, 0))
        x_line.set_stroke(YELLOW, 3)

        arrow = Vector(DOWN)
        arrow.next_to(s_part, DOWN, SMALL_BUFF)
        value = DecimalNumber(0, num_decimal_places=4)
        value.set_color(YELLOW)
        value.next_to(arrow, DOWN)

        self.add(axes)
        self.add(p_label)
        self.play(
            s_part.next_to, x_line.get_start(), UR, SMALL_BUFF,
            GrowArrow(arrow),
            FadeInFromPoint(value, s_part.get_center()),
        )

        s_part.tracked = x_line
        value.tracked = x_line
        value.x_axis = axes.x_axis
        self.play(
            ShowCreation(x_line),
            UpdateFromFunc(
                s_part,
                lambda m: m.next_to(m.tracked.get_end(), UR, SMALL_BUFF)
            ),
            UpdateFromFunc(
                value,
                lambda m: m.set_value(
                    m.x_axis.p2n(m.tracked.get_end())
                )
            ),
            run_time=3,
        )
        self.wait()
        self.play(
            FadeOut(arrow),
            FadeOut(value),
        )

        self.p_label = p_label
        self.s_part = s_part
        self.value = value
        self.x_line = x_line
        self.axes = axes

    def show_arrows(self):
        axes = self.axes

        arrows = VGroup()
        arrow_template = Vector(DOWN)

        def get_arrow(s, denom):
            arrow = arrow_template.copy()
            arrow.set_height(4 / denom)
            arrow.move_to(axes.c2p(s, 0), DOWN)
            arrow.set_color(interpolate_color(
                GREY_A, GREY_C, random.random()
            ))
            return arrow

        for k in range(2, 50):
            for n in range(1, k):
                if np.gcd(n, k) != 1:
                    continue
                s = n / k
                arrows.add(get_arrow(s, k))
        for k in range(50, 1000):
            arrows.add(get_arrow(1 / k, k))
            arrows.add(get_arrow(1 - 1 / k, k))

        kw = {
            "lag_ratio": 0.5,
            "run_time": 5,
            "rate_func": lambda t: t**4,
        }
        arrows.save_state()
        for arrow in arrows:
            arrow.stretch(0, 0)
            arrow.set_stroke(width=0)
            arrow.set_opacity(0)
        self.play(Restore(arrows, **kw))
        self.play(LaggedStartMap(
            ApplyMethod, arrows,
            lambda m: (m.scale, 0, {"about_edge": DOWN}),
            **kw
        ))
        self.remove(arrows)
        self.wait()

    def show_discrete_probabilities(self):
        axes = self.axes

        x_lines = VGroup()
        dx = 0.01
        for x in np.arange(0, 1, dx):
            line = Line(
                axes.c2p(x, 0),
                axes.c2p(x + dx, 0),
            )
            line.set_stroke(BLUE, 3)
            line.generate_target()
            line.target.rotate(
                90 * DEGREES,
                about_point=line.get_start()
            )
            x_lines.add(line)

        self.add(x_lines)
        self.play(
            FadeOut(self.x_line),
            LaggedStartMap(
                MoveToTarget, x_lines,
            )
        )

        label = Integer(0)
        label.set_height(0.5)
        label.next_to(self.p_label[1], DOWN, LARGE_BUFF)
        unit = OldTex("\\%")
        unit.match_height(label)
        fix_percent(unit.family_members_with_points()[0])
        always(unit.next_to, label, RIGHT, SMALL_BUFF)

        arrow = Arrow()
        arrow.max_stroke_width_to_length_ratio = 1
        arrow.axes = axes
        arrow.label = label
        arrow.add_updater(lambda m: m.put_start_and_end_on(
            m.label.get_bottom() + MED_SMALL_BUFF * DOWN,
            m.axes.c2p(0.01 * m.label.get_value(), 0.03),
        ))

        self.add(label, unit, arrow)
        self.play(
            ChangeDecimalToValue(label, 99),
            run_time=5,
        )
        self.wait()
        self.play(*map(FadeOut, [label, unit, arrow]))

        # Show prior label
        p_label = self.p_label
        given_data = p_label[2:4]
        prior_label = OldTex("P(s)", tex_to_color_map={"s": YELLOW})
        prior_label.match_height(p_label)
        prior_label.move_to(p_label, DOWN, LARGE_BUFF)

        p_label.save_state()
        self.play(
            given_data.scale, 0.5,
            given_data.set_opacity, 0.5,
            given_data.to_corner, UR,
            Transform(p_label[:2], prior_label[:2]),
            Transform(p_label[-1], prior_label[-1]),
        )
        self.wait()

        # Zoom in on the y-values
        new_ticks = VGroup()
        new_labels = VGroup()
        dy = 0.01
        for y in np.arange(dy, 5 * dy, dy):
            height = get_norm(axes.c2p(0, dy) - axes.c2p(0, 0))
            tick = axes.y_axis.get_tick(y, SMALL_BUFF)
            label = DecimalNumber(y)
            label.match_height(axes.y_axis.numbers[0])
            always(label.next_to, tick, LEFT, SMALL_BUFF)

            new_ticks.add(tick)
            new_labels.add(label)

        for num in axes.y_axis.numbers:
            height = num.get_height()
            always(num.set_height, height, stretch=True)

        bars = VGroup()
        dx = 0.01
        origin = axes.c2p(0, 0)
        for x in np.arange(0, 1, dx):
            rect = Rectangle(
                width=get_norm(axes.c2p(dx, 0) - origin),
                height=get_norm(axes.c2p(0, dy) - origin),
            )
            rect.x = x
            rect.set_stroke(BLUE, 1)
            rect.set_fill(BLUE, 0.5)
            rect.move_to(axes.c2p(x, 0), DL)
            bars.add(rect)

        stretch_group = VGroup(
            axes.y_axis,
            bars,
            new_ticks,
            x_lines,
        )
        x_lines.set_height(
            bars.get_height(),
            about_edge=DOWN,
            stretch=True,
        )

        self.play(
            stretch_group.stretch, 25, 1, {"about_point": axes.c2p(0, 0)},
            VFadeIn(bars),
            VFadeIn(new_ticks),
            VFadeIn(new_labels),
            VFadeOut(x_lines),
            run_time=4,
        )

        highlighted_bars = bars.copy()
        highlighted_bars.set_color(YELLOW)
        self.play(
            LaggedStartMap(
                FadeIn, highlighted_bars,
                lag_ratio=0.5,
                rate_func=there_and_back,
            ),
            ShowCreationThenFadeAround(new_labels[0]),
            run_time=3,
        )
        self.remove(highlighted_bars)

        # Nmae as prior
        prior_name = OldTexText("Prior", " distribution")
        prior_name.set_height(0.6)
        prior_name.next_to(prior_label, DOWN, LARGE_BUFF)

        self.play(FadeInFromDown(prior_name))
        self.wait()

        # Show alternate distribution
        bars.save_state()
        for a, b in [(5, 2), (1, 6)]:
            dist = scipy.stats.beta(a, b)
            for bar, saved in zip(bars, bars.saved_state):
                bar.target = saved.copy()
                height = get_norm(axes.c2p(0.1 * dist.pdf(bar.x)) - axes.c2p(0, 0))
                bar.target.set_height(height, about_edge=DOWN, stretch=True)

            self.play(LaggedStartMap(MoveToTarget, bars, lag_ratio=0.00))
            self.wait()
        self.play(Restore(bars))
        self.wait()

        uniform_name = OldTexText("Uniform")
        uniform_name.match_height(prior_name)
        uniform_name.move_to(prior_name, DL)
        uniform_name.shift(RIGHT)
        uniform_name.set_y(bars.get_top()[1] + MED_SMALL_BUFF, DOWN)
        self.play(
            prior_name[0].next_to, uniform_name, RIGHT, MED_SMALL_BUFF, DOWN,
            FadeOut(prior_name[1], RIGHT),
            FadeIn(uniform_name, LEFT)
        )
        self.wait()

        self.bars = bars
        self.uniform_label = VGroup(uniform_name, prior_name[0])

    def show_bayes_formula(self):
        uniform_label = self.uniform_label
        p_label = self.p_label
        bars = self.bars

        prior_label = VGroup(
            p_label[0].deepcopy(),
            p_label[1].deepcopy(),
            p_label[4].deepcopy(),
        )
        eq = OldTex("=")
        likelihood_label = OldTex(
            "P(", "\\text{data}", "|", "s", ")",
        )
        likelihood_label.set_color_by_tex("data", GREEN)
        likelihood_label.set_color_by_tex("s", YELLOW)
        over = Line(LEFT, RIGHT)
        p_data_label = OldTexText("P(", "\\text{data}", ")")
        p_data_label.set_color_by_tex("data", GREEN)

        for mob in [eq, likelihood_label, over, p_data_label]:
            mob.scale(1.5)
            mob.set_opacity(0.1)

        eq.move_to(prior_label, LEFT)
        over.set_width(
            prior_label.get_width() +
            likelihood_label.get_width() +
            MED_SMALL_BUFF
        )
        over.next_to(eq, RIGHT, MED_SMALL_BUFF)
        p_data_label.next_to(over, DOWN, MED_SMALL_BUFF)
        likelihood_label.next_to(over, UP, MED_SMALL_BUFF, RIGHT)

        self.play(
            p_label.restore,
            p_label.next_to, eq, LEFT, MED_SMALL_BUFF,
            prior_label.next_to, over, UP, MED_SMALL_BUFF, LEFT,
            FadeIn(eq),
            FadeIn(likelihood_label),
            FadeIn(over),
            FadeIn(p_data_label),
            FadeOut(uniform_label),
        )

        # Show new distribution
        post_bars = bars.copy()
        total_prob = 0
        for bar, p in zip(post_bars, np.arange(0, 1, 0.01)):
            prob = scipy.stats.binom(50, p).pmf(48)
            bar.stretch(prob, 1, about_edge=DOWN)
            total_prob += 0.01 * prob
        post_bars.stretch(1 / total_prob, 1, about_edge=DOWN)
        post_bars.stretch(0.25, 1, about_edge=DOWN)  # Lie to fit on screen...
        post_bars.set_color(MAROON_D)
        post_bars.set_fill(opacity=0.8)

        brace = Brace(p_label, DOWN)
        post_word = brace.get_text("Posterior")
        post_word.scale(1.25, about_edge=UP)
        post_word.set_color(MAROON_D)

        self.play(
            ReplacementTransform(
                bars.copy().set_opacity(0),
                post_bars,
            ),
            GrowFromCenter(brace),
            FadeIn(post_word, 0.25 * UP)
        )
        self.wait()
        self.play(
            eq.set_opacity, 1,
            likelihood_label.set_opacity, 1,
        )
        self.wait()

        data = get_check_count_label(48, 2)
        data.scale(1.5)
        data.next_to(likelihood_label, DOWN, buff=2, aligned_edge=LEFT)
        data_arrow = Arrow(
            likelihood_label[1].get_bottom(),
            data.get_top()
        )
        data_arrow.set_color(GREEN)

        self.play(
            GrowArrow(data_arrow),
            GrowFromPoint(data, data_arrow.get_start()),
        )
        self.wait()
        self.play(FadeOut(data_arrow))
        self.play(
            over.set_opacity, 1,
            p_data_label.set_opacity, 1,
        )
        self.wait()

        self.play(
            FadeOut(brace),
            FadeOut(post_word),
            FadeOut(post_bars),
            FadeOut(data),
            p_label.set_opacity, 0.1,
            eq.set_opacity, 0.1,
            likelihood_label.set_opacity, 0.1,
            over.set_opacity, 0.1,
            p_data_label.set_opacity, 0.1,
        )

        self.bayes = VGroup(
            p_label, eq,
            prior_label, likelihood_label,
            over, p_data_label
        )
        self.data = data

    def parallel_universes(self):
        bars = self.bars

        cols = VGroup()
        squares = VGroup()
        sample_colors = color_gradient(
            [GREEN_C, GREEN_D, GREEN_E],
            100
        )
        for bar in bars:
            n_rows = 12
            col = VGroup()
            for x in range(n_rows):
                square = Rectangle(
                    width=bar.get_width(),
                    height=bar.get_height() / n_rows,
                )
                square.set_stroke(width=0)
                square.set_fill(opacity=1)
                square.set_color(random.choice(sample_colors))
                col.add(square)
                squares.add(square)
            col.arrange(DOWN, buff=0)
            col.move_to(bar)
            cols.add(col)
        squares.shuffle()

        self.play(
            LaggedStartMap(
                VFadeInThenOut, squares,
                lag_ratio=0.005,
                run_time=3
            )
        )
        self.remove(squares)
        squares.set_opacity(1)
        self.wait()

        example_col = cols[95]

        self.play(
            bars.set_opacity, 0.25,
            FadeIn(example_col, lag_ratio=0.1),
        )
        self.wait()

        dist = scipy.stats.binom(50, 0.95)
        for x in range(12):
            square = random.choice(example_col).copy()
            square.set_fill(opacity=0)
            square.set_stroke(YELLOW, 2)
            self.add(square)
            nc = dist.ppf(random.random())
            data = get_check_count_label(nc, 50 - nc)
            data.next_to(example_col, UP)

            self.add(square, data)
            self.wait(0.5)
            self.remove(square, data)
        self.wait()

        self.data.set_opacity(1)
        self.play(
            FadeIn(self.data),
            FadeOut(example_col),
            self.bayes[3].set_opacity, 1,
        )
        self.wait()

    def update_from_data(self):
        bars = self.bars
        data = self.data
        bayes = self.bayes

        new_bars = bars.copy()
        new_bars.set_stroke(opacity=1)
        new_bars.set_fill(opacity=0.8)
        for bar, p in zip(new_bars, np.arange(0, 1, 0.01)):
            dist = scipy.stats.binom(50, p)
            scalar = dist.pmf(48)
            bar.stretch(scalar, 1, about_edge=DOWN)

        self.play(
            ReplacementTransform(
                bars.copy().set_opacity(0),
                new_bars
            ),
            bars.set_fill, {"opacity": 0.1},
            bars.set_stroke, {"opacity": 0.1},
            run_time=2,
        )

        # Show example bar
        bar95 = VGroup(
            bars[95].copy(),
            new_bars[95].copy()
        )
        bar95.save_state()
        bar95.generate_target()
        bar95.target.scale(2)
        bar95.target.next_to(bar95, UP, LARGE_BUFF)
        bar95.target.set_stroke(BLUE, 3)

        ex_label = OldTex("s", "=", "0.95")
        ex_label.set_color(YELLOW)
        ex_label.next_to(bar95.target, DOWN, submobject_to_align=ex_label[-1])

        highlight = SurroundingRectangle(bar95, buff=0)
        highlight.set_stroke(YELLOW, 2)

        self.play(FadeIn(highlight))
        self.play(
            MoveToTarget(bar95),
            FadeInFromDown(ex_label),
            data.shift, LEFT,
        )
        self.wait()

        side_brace = Brace(bar95[1], RIGHT, buff=SMALL_BUFF)
        side_label = side_brace.get_text("0.26", buff=SMALL_BUFF)
        self.play(
            GrowFromCenter(side_brace),
            FadeIn(side_label)
        )
        self.wait()
        self.play(
            FadeOut(side_brace),
            FadeOut(side_label),
            FadeOut(ex_label),
        )
        self.play(
            bar95.restore,
            bar95.set_opacity, 0,
        )

        for bar in bars[94:80:-1]:
            highlight.move_to(bar)
            self.wait(0.5)
        self.play(FadeOut(highlight))
        self.wait()

        # Emphasize formula terms
        tops = VGroup()
        for bar, new_bar in zip(bars, new_bars):
            top = Line(bar.get_corner(UL), bar.get_corner(UR))
            top.set_stroke(YELLOW, 2)
            top.generate_target()
            top.target.move_to(new_bar, UP)
            tops.add(top)

        rect = SurroundingRectangle(bayes[2])
        rect.set_stroke(YELLOW, 1)
        rect.target = SurroundingRectangle(bayes[3])
        rect.target.match_style(rect)
        self.play(
            ShowCreation(rect),
            ShowCreation(tops),
        )
        self.wait()
        self.play(
            LaggedStartMap(
                MoveToTarget, tops,
                run_time=2,
                lag_ratio=0.02,
            ),
            MoveToTarget(rect),
        )
        self.play(FadeOut(tops))
        self.wait()

        # Show alternate priors
        axes = self.axes
        bar_groups = VGroup()
        for bar, new_bar in zip(bars, new_bars):
            bar_groups.add(VGroup(bar, new_bar))

        bar_groups.save_state()
        for a, b in [(5, 2), (7, 1)]:
            dist = scipy.stats.beta(a, b)
            for bar, saved in zip(bar_groups, bar_groups.saved_state):
                bar.target = saved.copy()
                height = get_norm(axes.c2p(0.1 * dist.pdf(bar[0].x)) - axes.c2p(0, 0))
                height = max(height, 1e-6)
                bar.target.set_height(height, about_edge=DOWN, stretch=True)

            self.play(LaggedStartMap(MoveToTarget, bar_groups, lag_ratio=0))
            self.wait()
        self.play(Restore(bar_groups))
        self.wait()

        # Rescale
        ex_p_label = OldTex(
            "P(s = 0.95 | 00000000) = ",
            tex_to_color_map={
                "s = 0.95": YELLOW,
                "00000000": WHITE,
            }
        )
        ex_p_label.scale(1.5)
        ex_p_label.next_to(bars, UP, LARGE_BUFF)
        ex_p_label.align_to(bayes, LEFT)
        template = ex_p_label.get_part_by_tex("00000000")
        template.set_opacity(0)

        highlight = SurroundingRectangle(new_bars[95], buff=0)
        highlight.set_stroke(YELLOW, 1)

        self.remove(data)
        self.play(
            FadeIn(ex_p_label),
            VFadeOut(data[0]),
            data[1:].move_to, template,
            FadeIn(highlight)
        )
        self.wait()

        numer = new_bars[95].copy()
        numer.set_stroke(YELLOW, 1)
        denom = new_bars[80:].copy()
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(3)
        h_line.set_stroke(width=2)
        h_line.next_to(ex_p_label, RIGHT)

        self.play(
            numer.next_to, h_line, UP,
            denom.next_to, h_line, DOWN,
            ShowCreation(h_line),
        )
        self.wait()
        self.play(
            denom.space_out_submobjects,
            rate_func=there_and_back
        )
        self.play(
            bayes[4].set_opacity, 1,
            bayes[5].set_opacity, 1,
            FadeOut(rect),
        )
        self.wait()

        # Rescale
        self.play(
            FadeOut(highlight),
            FadeOut(ex_p_label),
            FadeOut(data),
            FadeOut(h_line),
            FadeOut(numer),
            FadeOut(denom),
            bayes.set_opacity, 1,
        )

        # CHANGE: unlock_shader_data no longer exists in manimgl (there is no locked shader data); it is removed
        pass
        self.remove(new_bars, *new_bars)
        self.play(
            new_bars.set_height, 5, {"about_edge": DOWN, "stretch": True},
            new_bars.set_color, MAROON_D,
        )
        self.wait()
