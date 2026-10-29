# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2023/convolutions2/diagonal_slices.py (lines 990-1016)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/clt/main.py, _2023/convolutions2/continuous.py
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING


# ----- From _2023/clt/main.py -----

if TYPE_CHECKING:
    from typing import Sequence
    from manimlib.typing import ManimColor


EXP_DISTRIBUTION = [0.41, 0.25, 0.15, 0.10, 0.06, 0.03]


U_SHAPED_DISTRIBUTION = [0.3, 0.15, 0.05, 0.05, 0.15, 0.3]


STEEP_U_SHAPED_DISTRIBUTION = [0.4, 0.075, 0.025, 0.025, 0.075, 0.4]


class ChartBars(VGroup):
    def __init__(
        self,
        axes,
        values: Sequence[float | int],
        xs: Sequence[float] | None = None,
        width_ratio: float = 1.0,
        offset: float = 0.5,
        fill_color: ManimColor = BLUE,
        fill_opacity: float = 0.5,
        stroke_color: ManimColor = WHITE,
        stroke_width: float = 1.0
    ):
        xs = xs if xs is not None else np.arange(*axes.x_range)

        self.x_to_index = dict(zip(xs, it.count()))
        x_step = xs[1] - xs[0]
        x_unit = axes.x_axis.get_unit_size()
        y_unit = axes.y_axis.get_unit_size()

        width = width_ratio * x_unit * x_step

        # Create a list of rectangles arranged side by side,
        # one for each x value
        rects = []
        epsilon = 1e-8
        for x, y in zip(xs, values):
            rect = Rectangle(
                width=width,
                height=max(y * y_unit, epsilon),
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
            )
            rect.move_to(axes.c2p(x + offset * x_step, 0), DOWN)
            rects.append(rect)
        super().__init__(*rects)
        self.axes = axes
        self.xs = xs
        self.set_values(values)

    def set_values(self, values: Iterable[float | int]):
        y_unit = self.axes.y_axis.get_unit_size()
        for rect, value in zip(self, values):
            rect.set_height(
                y_unit * value,
                stretch=True,
                about_edge=DOWN,
            )


def get_dist(bars):
    result = np.array([bar.get_height() for bar in bars])
    return result / result.sum()


def get_mean_and_sd(dist, x_min=1):
    mean = sum(p * (n + x_min) for n, p in enumerate(dist))
    sd = math.sqrt(sum(p * (n + x_min - mean)**2 for n, p in enumerate(dist)))
    return mean, sd


def gauss_func(x, mu, sigma):
    pre_factor = 1 / (sigma * math.sqrt(2 * PI))
    return pre_factor * np.exp(-0.5 * ((x - mu) / sigma)**2)


class LimitingDistributions(InteractiveScene):
    distribution = EXP_DISTRIBUTION
    x_min = 1
    bar_colors = (BLUE, TEAL)
    bar_opacity = 0.75
    y_range = (0, 0.5, 0.1)
    max_n = 50
    normal_y_range = (0, 0.5, 0.25)
    normal_axes_height = 2

    def construct(self):
        # Dividing line
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH)
        h_line.set_stroke(GREY, 2)
        self.add(h_line)

        # Starting distribution
        dist = np.array(self.distribution)
        dist /= dist.sum()
        top_plot = self.get_top_distribution_plot(dist)
        top_label = TexText(R"Random variable \\ $X$", font_size=36)
        top_label[-1].scale(1.2, about_edge=UP).shift(0.25 * DOWN)
        top_label.move_to(top_plot).to_edge(LEFT, buff=0.25).shift(0.35 * UP)
        self.add(top_plot)
        self.add(top_label)

        # Lower plot
        N_tracker = ValueTracker(2)
        get_N = lambda: int(N_tracker.get_value())
        s_plot = self.get_sum_plot(dist, get_N(), top_plot)  # TODO
        self.add(s_plot)

        # Mean and s.d. labels
        bars = top_plot.bars
        mean, sd = get_mean_and_sd(get_dist(bars))
        top_mean_sd_labels = self.get_mean_sd_labels(
            R"\mu", R"\sigma", mean, sd
        )
        sum_mean_sd_labels = self.get_mean_sd_labels(
            R"\mu \cdot N", R"\sigma \cdot \sqrt{N}",
            mean * 10, sd * math.sqrt(10),
        )
        scaled_sum_mean_sd_labels = self.get_mean_sd_labels(R"", R"", 0, 1)

        sum_mean_sd_labels.next_to(h_line, DOWN)
        sum_mean_sd_labels.to_edge(RIGHT)
        scaled_sum_mean_sd_labels.next_to(h_line, DOWN)
        scaled_sum_mean_sd_labels.align_to(sum_mean_sd_labels, LEFT)
        top_mean_sd_labels.next_to(TOP, DOWN)
        top_mean_sd_labels.align_to(sum_mean_sd_labels, LEFT)

        mu_label, sigma_label = self.get_mu_sigma_annotations(top_plot)

        # Lower distribution labels
        sum_label = self.get_sum_label(get_N())
        self.add(sum_label)

        # Increase N
        for n in range(3, 11):
            new_s_plot = self.get_sum_plot(dist, n, top_plot)
            new_sum_label = self.get_sum_label(n, dots=False)
            N_tracker.set_value(n)
            self.play(
                ReplacementTransform(s_plot.bars, new_s_plot.bars[:len(s_plot.bars)]),
                GrowFromEdge(new_s_plot.bars[len(s_plot.bars):], DOWN),
                ReplacementTransform(s_plot.axes, new_s_plot.axes),
                FadeTransform(sum_label, new_sum_label),
                run_time=0.5,
            )
            s_plot = new_s_plot
            sum_label = new_sum_label
            self.wait(0.5)

        self.wait()

        # Show mean and standard deviation
        self.play(Write(mu_label, stroke_color=PINK), run_time=1)
        self.play(TransformMatchingTex(mu_label[1].copy(), top_mean_sd_labels[0]), run_time=1)
        self.wait()

        sigma_label.save_state()
        sigma_label.stretch(0, 0).set_opacity(0)
        self.play(Restore(sigma_label))
        self.play(TransformMatchingTex(sigma_label[2].copy(), top_mean_sd_labels[1]), run_time=1)
        self.wait()

        low_mu_label, low_sigma_label = self.get_mu_sigma_annotations(s_plot)
        low_lines = VGroup(low_mu_label[0], low_sigma_label[0])
        low_lines.shift((get_N() - 1.5)* s_plot.axes.x_axis.get_unit_size() * RIGHT)
        low_lines.stretch(0.5, 1, about_edge=DOWN)
        new_sum_label = self.get_sum_label(get_N())

        sum_mean_sd_labels.update()
        self.play(
            TransformMatchingTex(top_mean_sd_labels[0].copy(), sum_mean_sd_labels[0]),
            TransformMatchingTex(sum_label, new_sum_label),
            TransformFromCopy(mu_label[:1], low_mu_label[:1]),
            run_time=1.5
        )
        sum_label = new_sum_label
        self.wait()
        self.play(
            TransformMatchingTex(top_mean_sd_labels[1].copy(), sum_mean_sd_labels[1]),
            TransformFromCopy(sigma_label[:1], low_sigma_label[:1]),
            run_time=1.5
        )
        self.wait()

        # Write formula
        formula = Tex(
            R"{1 \over \sigma \sqrt{2\pi N}} e^{-{1 \over 2} \left({x - \mu N \over \sigma \sqrt{N}} \right)^2}",
            t2c={
                R"\mu": PINK,
                R"\sigma": RED,
                R"N": YELLOW,
            },
            font_size=36
        )
        N = get_N()
        mu, sigma = get_mean_and_sd(get_dist(s_plot.bars), x_min=N)
        graph = s_plot.axes.get_graph(lambda x: gauss_func(x, mu - 1, sigma))
        graph.set_stroke(WHITE, 3)
        formula.next_to(graph, UP).align_to(graph, LEFT).shift(0.5 * RIGHT)

        self.play(
            ShowCreation(graph),
            FadeIn(formula, UP),
        )
        self.wait()
        self.play(LaggedStartMap(
            FadeOut,
            VGroup(graph, *low_lines, formula),
            lag_ratio=0.5
        ))

        # Transition to rescaled version
        scaled_sum_label = self.get_sum_label(get_N(), scaled=True)
        ss_plot = self.get_scaled_sum_plot(dist, get_N())
        x_shift = 2 * RIGHT

        self.play(FlashAround(sum_label, time_width=1.5, run_time=2))
        self.play(LaggedStart(
            Transform(
                sum_label,
                scaled_sum_label[sum_label.get_string()][0].copy(),
                remover=True,
            ),
            Write(scaled_sum_label),
            s_plot.animate.shift(x_shift),
            lag_ratio=0.5
        ))
        self.wait()

        sub_part = scaled_sum_label[R"- \decimalmob \cdot \mu"]
        rect = SurroundingRectangle(sum_mean_sd_labels[0], color=RED)
        target_x = ss_plot.axes.c2p(0, 0)[0]
        self.play(ShowCreation(rect))
        self.play(
            FadeTransform(sum_mean_sd_labels[0].copy(), sub_part),
            rect.animate.set_points(SurroundingRectangle(sub_part).get_points()),
            s_plot.bars.animate.shift((target_x - low_lines[0].get_x() - x_shift) * RIGHT),
            s_plot.axes.animate.shift((target_x - s_plot.axes.c2p(0, 0)[0]) * RIGHT),
        )
        self.play(
            FadeOut(rect),
            FadeOut(sum_mean_sd_labels[0], RIGHT),
            FadeIn(scaled_sum_mean_sd_labels[0], RIGHT)
        )
        self.wait()

        div_part = scaled_sum_label[R"\sigma \cdot \sqrt{\decimalmob}"]
        rect = SurroundingRectangle(sum_mean_sd_labels[1], color=RED)
        self.play(ShowCreation(rect))
        self.play(
            FadeTransform(sum_mean_sd_labels[1].copy(), div_part),
            rect.animate.set_points(SurroundingRectangle(div_part).get_points()),
        )
        self.play(FadeOut(rect))
        self.wait()

        # Swap to new axes
        stretch_group = VGroup(ss_plot.axes.y_axis, ss_plot.bars)
        stretch_factor = s_plot.bars.get_height() / ss_plot.bars.get_height()
        stretch_group.stretch(stretch_factor, dim=1, about_edge=DOWN)

        self.play(
            FadeOut(s_plot.axes),
            FadeIn(ss_plot.axes),
            ReplacementTransform(s_plot.bars, ss_plot.bars),
            FadeOut(sum_label)
        )
        self.play(stretch_group.animate.stretch(1 / stretch_factor, dim=1, about_edge=DOWN))
        self.wait()

        # Show sd of 1
        sd_lines = Line(DOWN, UP).replicate(2)
        sd_lines[0].move_to(ss_plot.axes.c2p(1, 0), DOWN)
        sd_lines[1].move_to(ss_plot.axes.c2p(-1, 0), DOWN)
        sd_lines.set_stroke(RED, 3)
        sd_lines.save_state()
        sd_lines.stretch(0, 0).set_opacity(0)
        self.play(
            Restore(sd_lines),
            FadeOut(sum_mean_sd_labels[1], RIGHT),
            FadeIn(scaled_sum_mean_sd_labels[1], RIGHT)
        )
        self.wait()
        self.play(FadeOut(sd_lines))

        # Readable meaning
        full_screen_rect = FullScreenFadeRectangle()
        full_screen_rect.set_opacity(0.7)
        top_rect = full_screen_rect.copy().stretch(0.5, 1, about_edge=UP)
        top_rect.set_fill(BLACK, 0.7)
        words = Text("Highly readable meaning:")
        words.next_to(scaled_sum_label, UP, LARGE_BUFF, aligned_edge=LEFT)
        meaning = TexText(
            R"How many std devs away from the mean is $X_1 + \cdots + X_{10}$",
            t2c={"std devs": RED, "mean": PINK, },
            font_size=40
        )
        meaning.move_to(words, LEFT)

        self.add(full_screen_rect, scaled_sum_label)
        self.play(FadeIn(full_screen_rect))
        self.wait()
        self.play(
            FadeIn(top_rect), FadeIn(words)
        )
        self.wait()
        self.play(
            words.animate.shift(UP),
            Write(meaning)
        )
        self.wait()

        # Example bar
        bar = ss_plot.bars[9].copy()
        ss_plot.bars.save_state()

        sum_tex = Tex(R"0 = 19")
        die = DieFace(1, fill_color=BLUE_E)
        die.dots.set_opacity(0)
        dice = die.get_grid(2, 5)
        dice.set_height(0.75)
        dice.set_stroke(width=1)
        dice.move_to(sum_tex[0], RIGHT)
        sum_tex.replace_submobject(0, dice)
        sum_tex.move_to(bar).to_edge(LEFT)

        arrow = Arrow(sum_tex, bar, buff=0.1)

        ss_plot.bars.set_opacity(0.2)
        self.play(
            FadeOut(full_screen_rect),
            top_rect.animate.set_opacity(1),
            FadeIn(bar)
        )
        self.wait()
        self.play(
            FadeIn(sum_tex, lag_ratio=0.2, run_time=2),
            GrowArrow(arrow),
        )
        self.wait()
        self.play(
            arrow.animate.become(Vector(0.5 * UP).next_to(bar, DOWN, SMALL_BUFF))
        )
        self.wait()
        self.play(LaggedStart(
            FadeOut(top_rect),
            Restore(ss_plot.bars),
            FadeOut(bar),
            FadeOut(words),
            FadeOut(meaning),
            FadeOut(sum_tex),
            FadeOut(arrow),
        ))

        # Comment on meaning of bars
        words = Text("Probability = Area", font_size=36)
        words.next_to(bar, LEFT, buff=1.5, aligned_edge=UP)
        arrow = Arrow(words.get_right(), bar.get_center())

        y_axis_label = Text("Probability\ndensity", font_size=24)
        y_axis_label.set_color(GREY_B)
        y_axis_label.next_to(ss_plot.axes.c2p(0, 0.5), RIGHT, SMALL_BUFF)

        bar_range = ss_plot.bars[8:16].copy()

        self.play(
            ss_plot.bars.animate.set_opacity(0.2),
            FadeIn(bar)
        )
        self.play(FlashAround(scaled_sum_label))
        self.wait()
        self.play(Write(words), ShowCreation(arrow))
        self.wait()
        self.play(FadeIn(y_axis_label, 0.2 * UP))
        self.wait()
        self.play(
            FadeIn(bar_range, lag_ratio=0.2),
            FadeOut(bar)
        )
        self.wait()
        self.play(
            Restore(ss_plot.bars),
            FadeOut(bar_range)
        )
        self.wait()
        self.play(FadeOut(words), FadeOut(arrow), FadeOut(y_axis_label))

        # Roll back to 3
        for n in range(9, 2, -1):
            new_scaled_sum_label = self.get_sum_label(n, scaled=True)
            new_ss_plot = self.get_scaled_sum_plot(dist, n)
            N_tracker.set_value(n)

            self.remove(ss_plot.axes)
            self.add(new_ss_plot.axes)
            self.play(
                FadeTransform(scaled_sum_label, new_scaled_sum_label),
                FadeTransform(ss_plot.bars, new_ss_plot.bars),
                run_time=0.1
            )
            self.wait(0.4)

            scaled_sum_label = new_scaled_sum_label
            ss_plot = new_ss_plot

        # Mess around with the distribution
        alt_dists = [
            np.array(U_SHAPED_DISTRIBUTION),
            np.random.random(6),
            np.random.random(6),
            np.array(STEEP_U_SHAPED_DISTRIBUTION),
            np.random.random(6),
        ]
        for dist in alt_dists:
            dist /= dist.sum()

        words = Text("Change this\ndistribution")
        words.set_color(YELLOW)
        words.move_to(top_plot, UR)

        self.play(
            FadeOut(mu_label),
            FadeOut(sigma_label),
            Write(words),
        )
        self.change_distribution(
            alt_dists, top_plot, ss_plot,
            top_mean_sd_labels, get_N()
        )
        self.play(FadeOut(words))

        # Show limit
        for n in range(4, self.max_n + 1):
            N_tracker.set_value(n)
            new_ss_plot = self.get_scaled_sum_plot(self.distribution, n)
            new_scaled_sum_label = self.get_sum_label(n, scaled=True)

            if n < 5:
                rt = 0.5
                wt = 0.25
            elif n < 15:
                rt = 0.1
                wt = 0.1
            else:
                rt = 0
                wt = 0.1

            if rt > 0:
                self.play(
                    FadeOut(ss_plot.bars),
                    FadeIn(new_ss_plot.bars),
                    ReplacementTransform(ss_plot.axes, new_ss_plot.axes),
                    FadeTransform(scaled_sum_label, new_scaled_sum_label),
                    run_time=rt
                )
            else:
                self.remove(ss_plot, scaled_sum_label)
                self.add(new_ss_plot, new_scaled_sum_label)
            self.wait(wt)
            ss_plot = new_ss_plot
            scaled_sum_label = new_scaled_sum_label

            if n in [10, self.max_n]:
                # More switching
                self.wait()
                self.change_distribution(
                    [EXP_DISTRIBUTION, *alt_dists],
                    top_plot,
                    ss_plot,
                    top_mean_sd_labels, get_N(),
                )

        self.wait()

        # Show standard normal graph
        graph = ss_plot.axes.get_graph(
            lambda x: gauss_func(x, 0, 1),
            x_range=(-8, 8)
        )
        graph.set_stroke(YELLOW, 3)
        label = Tex(R"{1 \over \sqrt{2\pi}} e^{-x^2 / 2}")
        label[R"{1 \over \sqrt{2\pi}}"].scale(0.8, about_edge=RIGHT)
        label.next_to(graph.pfp(0.55), UR)

        self.play(
            ShowCreation(graph),
            Write(label),
            scaled_sum_mean_sd_labels.animate.to_edge(RIGHT)
        )
        self.play(FlashAround(label, run_time=2))
        self.wait()

        random_dists = [normalize(np.random.random(6))**2 for x in range(8)]
        self.change_distribution(
            [*random_dists, alt_dists[-1]],
            top_plot,
            ss_plot,
            top_mean_sd_labels, get_N(),
            run_time=1.5
        )
        self.wait()

        # Formal statement
        gen_scaled_sum_label = self.get_sum_label("N", scaled=True)
        gen_scaled_sum_label.replace(new_scaled_sum_label)
        rect = SurroundingRectangle(gen_scaled_sum_label)
        rect.set_stroke(BLUE, 2)
        statement = Tex(
            R"\lim_{N \to \infty} P(a < \text{This value} < b) = \int_a^b " + label.get_string() + "dx",
            font_size=36
        )
        statement["N"].set_color(YELLOW)
        statement.next_to(rect, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        arrow = Arrow(statement["This value"], rect, buff=0.1)
        arrow.set_color(BLUE)

        bars = ss_plot.bars
        mid_i = np.argmax([bar.get_height() for bar in bars])
        to_fade = VGroup(*bars[:mid_i - 5], *bars[mid_i + 10:])

        shift_group = VGroup(ss_plot, graph)

        self.play(ShowCreation(rect))
        self.play(ReplacementTransform(new_scaled_sum_label, gen_scaled_sum_label))
        self.wait()
        self.play(
            FadeIn(statement[R"P(a < \text{This value} < b)"], 0.5 * DOWN)
        )
        self.play(
            statement["This value"].animate.set_color(BLUE),
            ShowCreation(arrow)
        )
        self.play(
            to_fade.animate.set_fill(opacity=0.1).set_stroke(width=0),
            graph.animate.set_stroke(width=1.5),
        )
        self.wait()
        self.play(Write(statement[R"\lim_{N \to \infty}"]))
        self.wait()
        self.play(LaggedStart(
            shift_group.animate.shift(3 * RIGHT),
            FadeTransform(label, statement[label.get_string()]),
            Write(statement[R" = \int_a^b "]),
            Write(statement[R"dx"]),
            lag_ratio=0.4,
            run_time=3,
        ))
        self.wait()

        self.play(LaggedStart(*(
            Indicate(bar, color=BLUE)
            for bar in bars[mid_i - 5:mid_i + 10]
        )))
        self.wait()

    def get_top_distribution_plot(
        self,
        dist,
        width=5,
        height=2.5,
        y_range=(0, 0.5, 0.1)
    ):
        # Axes and bars
        x_min = self.x_min

        axes = Axes(
            (x_min - 1, x_min + len(dist) - 1),
            y_range,
            width=width,
            height=height,
        )
        axes.x_axis.add_numbers(font_size=24, excluding=[0])
        axes.x_axis.numbers.shift(0.5 * axes.x_axis.get_unit_size() * LEFT)
        axes.y_axis.add_numbers(num_decimal_places=1, font_size=24, excluding=[0])

        bars = ChartBars(axes, dist)
        bars.set_submobject_colors_by_gradient(*self.bar_colors)
        bars.set_opacity(self.bar_opacity)

        plot = VGroup(axes, bars)
        plot.move_to(LEFT).to_edge(UP)

        plot.axes = axes
        plot.bars = bars

        return plot

    def get_mu_sigma_annotations(self, plot, mu_tex=R"\mu", sigma_tex=R"\sigma", min_height=2.0, x_min=1):
        bars = plot.bars
        axes = plot.axes
        dist = get_dist(bars)

        mu, sigma = get_mean_and_sd(dist, x_min)
        mean_line = Line(DOWN, UP)
        mean_line.set_height(max(bars.get_height() + 0.25, min_height))
        mean_line.set_stroke(PINK, 2)
        mean_line.move_to(axes.c2p(mu - 0.5, 0), DOWN)

        sd_lines = Line(DOWN, UP).replicate(2)
        sd_lines.arrange(RIGHT)
        sd_lines.set_stroke(RED, 2)
        sd_lines.match_height(mean_line)
        sd_lines[0].move_to(axes.c2p(mu - sigma - 0.5, 0), DOWN)
        sd_lines[1].move_to(axes.c2p(mu + sigma - 0.5, 0), DOWN)

        sd_arrows = VGroup(Vector(LEFT, stroke_width=3), Vector(RIGHT, stroke_width=3))
        sd_arrows.arrange(RIGHT, buff=0.25)
        sd_arrows.set_width(0.85 * sd_lines.get_width())
        sd_arrows.move_to(mean_line.pfp(0.75))
        sd_arrows.set_color(RED)

        mu_label = Tex(mu_tex, color=PINK, font_size=30)
        mu_label.next_to(mean_line, UP, SMALL_BUFF)
        sigma_label = Tex(sigma_tex, color=RED, font_size=30)
        sigma_label.set_max_width(sd_arrows[1].get_width() * 0.8)
        sigma_label.next_to(sd_arrows[1], UP, SMALL_BUFF)

        return (
            VGroup(mean_line, mu_label),
            VGroup(sd_lines, sd_arrows, sigma_label),
        )

    def get_sum_label(self, n: str | int, dots=True, scaled: bool = False):
        if isinstance(n, int) and n not in [2, 3]:
            if len(str(n)) == 1:
                n_str = "0"
            else:
                n_str = "1" + "0" * (len(str(n)) - 1)
        else:
            n_str = str(n)

        if n_str == "2":
            sum_tex = R"X_1 + X_2"
        elif n_str == "3":
            sum_tex = R"X_1 + X_2 + X_3"
        elif dots:
            sum_tex = Rf"X_1 + \cdots + X_{{{n_str}}}"
        else:
            sum_tex = " + ".join(f"X_{{{k}}}" for k in range(1, int(n) + 1))

        if scaled:
            sum_tex = "(" + sum_tex + ")" + Rf" - {n_str} \cdot \mu \over \sigma \cdot \sqrt{{{n_str}}}"

        sum_label = Tex(
            sum_tex,
            t2c={
                R"\mu": PINK,
                R"\sigma": RED,
                n_str: YELLOW,
            },
            font_size=40
        )

        if scaled:
            sum_label.scale(0.8)

        if isinstance(n, int) and n_str in sum_label.get_string():
            n_parts = sum_label.make_number_changeable(n_str, replace_all=True)
            for part in n_parts:
                part.set_value(n)

        sum_label.next_to(ORIGIN, DOWN)
        sum_label.to_edge(LEFT)
        return sum_label

    def get_scaled_sum_plot(self, dist, n):
        sum_dist = np.array(dist)
        for _ in range(n - 1):
            sum_dist = np.convolve(sum_dist, dist)

        axes = self.get_normal_plot_axes()

        mu, sigma = get_mean_and_sd(dist)
        x_min = n * self.x_min
        unscaled_xs = np.arange(x_min, x_min + len(sum_dist))
        xs = (unscaled_xs - n * mu) / (sigma * math.sqrt(n))

        bars = ChartBars(axes, sum_dist, xs=xs)
        bars.shift(0.5 * bars[0].get_width() * LEFT)
        bars.set_submobject_colors_by_gradient(*self.bar_colors)
        bars.set_opacity(self.bar_opacity)

        unit_area = axes.x_axis.get_unit_size() * axes.y_axis.get_unit_size()
        bar_area = sum(bar.get_width() * bar.get_height() for bar in bars)
        bars.stretch(unit_area / bar_area, 1, about_edge=DOWN)

        plot = VGroup(axes, bars)
        plot.set_stroke(background=True)

        plot.bars = bars
        plot.axes = axes

        return plot

    def get_normal_plot_axes(self):
        sum_axes = Axes(
            (-6, 6), self.normal_y_range,
            width=12, height=self.normal_axes_height
        )
        sum_axes.center().move_to(FRAME_HEIGHT * DOWN / 4)
        sum_axes.x_axis.add_numbers(font_size=16)
        sum_axes.y_axis.add_numbers(num_decimal_places=1, font_size=16, excluding=[0])
        return sum_axes

    def get_sum_plot(
        self,
        dist,
        n,
        top_plot,
        x_range=(0, 40),
        y_range=(0, 0.2, 0.1),
        x_num_range=(5, 40, 5),
        max_width=10,
    ):
        sum_dist = np.array(dist)
        for _ in range(n - 1):
            sum_dist = np.convolve(sum_dist, dist)

        x_min = n * self.x_min

        x_max = x_range[1]
        axes = Axes(
            x_range,
            y_range,
            width=top_plot.axes.x_axis.get_unit_size() * x_max,
            height=self.normal_axes_height,
            axis_config=dict(tick_size=0.05),
        )
        axes.x_axis.set_max_width(max_width, stretch=True, about_point=axes.c2p(0, 0))
        axes.shift(top_plot.axes.c2p(0, 0) - axes.c2p(0, 0))
        axes.to_edge(DOWN)
        axes.x_axis.add_numbers(np.arange(*x_num_range), font_size=16, excluding=[0])
        axes.x_axis.numbers.shift(0.5 * axes.x_axis.get_unit_size() * LEFT)
        axes.y_axis.add_numbers(
            num_decimal_places=len(str(y_range[2])) - 2,
            font_size=24,
            excluding=[0]
        )

        bars = ChartBars(axes, sum_dist, xs=range(x_min - 1, x_min + len(sum_dist) - 1))
        bars.set_submobject_colors_by_gradient(*self.bar_colors)
        bars.set_opacity(self.bar_opacity)

        plot = VGroup(axes, bars)
        plot.axes = axes
        plot.bars = bars

        return plot

    def get_mean_sd_labels(self, mu_tex, sigma_tex, mean, sd):
        label_kw = dict(
            t2c={
                R"\mu": PINK,
                R"\sigma": RED,
                R"N": YELLOW,
            },
            font_size=36
        )
        if len(mu_tex) > 0:
            mu_tex = "= " + mu_tex
        if len(sigma_tex) > 0:
            sigma_tex = "= " + sigma_tex

        labels = VGroup(
            Tex(Rf"\text{{mean}} {mu_tex} = 0.00", **label_kw),
            Tex(Rf"\text{{std dev}} {sigma_tex} = 0.00", **label_kw),
        )
        labels.arrange(DOWN, aligned_edge=LEFT)
        values = [mean, sd]
        colors = [PINK, RED]
        for label, value, color in zip(labels, values, colors):
            num = label.make_number_changeable("0.00")
            num.set_value(value)
            num.set_color(color)

        return labels

    def change_distribution(
        self,
        alt_dists,
        top_plot,
        ss_plot,
        top_mean_sd_labels,
        n,
        run_time=1,
    ):
        for dist in alt_dists:
            new_top_plot = self.get_top_distribution_plot(dist)
            new_top_plot.bars.align_to(top_plot.bars, DOWN)
            new_ss_plot = self.get_scaled_sum_plot(dist, n)
            mean, sd = get_mean_and_sd(dist)
            self.play(
                Transform(top_plot.bars, new_top_plot.bars),
                UpdateFromFunc(
                    ss_plot.bars,
                    lambda m: m.set_submobjects(self.get_scaled_sum_plot(
                        get_dist(top_plot.bars), n
                    ).bars)
                ),
                ChangeDecimalToValue(top_mean_sd_labels[0][-1], mean),
                ChangeDecimalToValue(top_mean_sd_labels[1][-1], sd),
             )
            self.wait()
            self.distribution = dist


class Thumbnail(LimitingDistributions):
    def construct(self):
        # Tests
        dist = [1 / 6] * 6
        ss_plot = self.get_scaled_sum_plot(dist, 50)
        for axis in ss_plot.axes:
            axis.remove(axis.numbers)
            for tick in axis.ticks:
                tick.scale(0.5)
        ss_plot.axes.y_axis.set_opacity(0)
        ss_plot.scale(2)
        ss_plot.bars.set_submobject_colors_by_gradient(
            *3 * [BLUE], *3 * [YELLOW]
        )
        ss_plot.shift(2 * DOWN - ss_plot.axes.c2p(0, 0))
        ss_plot.to_edge(DOWN)
        self.add(ss_plot)

        # Top plots
        top_plots = VGroup()
        np.random.seed(3)
        dists = [
            EXP_DISTRIBUTION,
            normalize(np.random.random(6))**2,
            normalize(np.random.random(6))**2,
            U_SHAPED_DISTRIBUTION,
        ]
        for dist in dists:
            top_plot = self.get_top_distribution_plot(dist, width=3, height=2, y_range=(0, 0.401, 0.1))
            for axis in top_plot.axes:
                axis.remove(axis.numbers)
            top_plots.add(top_plot)
            top_plot.bars.set_submobject_colors_by_gradient(BLUE_D, TEAL)
            top_plot.bars.set_stroke(WHITE, 1)
        top_plots.arrange(RIGHT, buff=2.0, aligned_edge=DOWN)
        top_plots.set_width(FRAME_WIDTH - 1)
        top_plots.to_edge(UP)

        arrows = VGroup(*(
            Arrow(
                tp.get_bottom(),
                ss_plot.bars.get_top() + vect,
                buff=0.3,
                stroke_width=10,
                stroke_color=YELLOW
            )
            for tp, vect in zip(top_plots, np.linspace(2 * LEFT, 2 * RIGHT, len(top_plots)))
        ))

        self.add(top_plots)
        self.add(arrows)

        # Words
        words = Text("Bizarrely\nUniversal", font_size=90)
        words.move_to(ss_plot.axes.c2p(0, 0.03), DOWN).to_edge(LEFT)
        words.set_x(0)
        words.set_backstroke()
        # self.add(words)

        # Formula
        form = Tex(R"{1 \over \sqrt{2\pi}} e^{-x^2 / 2}", font_size=90)
        form.move_to(words, DOWN).to_edge(RIGHT)



# ----- From _2023/convolutions2/continuous.py -----

def wedge_func(x):
    return np.clip(-np.abs(x) + 1, 0, 1)


def double_lump(x):
    return 0.45 * np.exp(-6 * (x - 0.5)**2) + np.exp(-6 * (x + 0.5)**2)



# ----- From _2023/convolutions2/diagonal_slices.py -----

class Introduce3DGraph(InteractiveScene):
    plane_config = dict(
        x_range=(-2, 2),
        y_range=(-2, 2),
        width=6.0,
        height=6.0,
    )
    plane_width = 6.0
    z_axis_height = 2.0
    plane_line_style = dict(
        stroke_color=GREY_C,
        stroke_width=1,
        stroke_opacity=1,
    )
    graph_resolution = (101, 101)

    def construct(self):
        # Initial axes and graphs
        f_axes, g_axes = all_axes = VGroup(*(
            Axes((-2, 2), (0, 1, 0.5), width=5, height=2)
            for n in range(2)
        ))
        all_axes.arrange(DOWN, buff=1.5)
        all_axes.to_edge(LEFT)
        self.frame.move_to(all_axes)

        for char, axes in zip("xy", all_axes):
            axis_label = Tex(char, font_size=24)
            axis_label.next_to(axes.x_axis.get_right(), UP)
            axes.add(axis_label)

        f_graph = f_axes.get_graph(self.f, use_smoothing=False)
        f_graph.set_stroke(BLUE, 3)
        g_graph = g_axes.get_graph(self.g)
        g_graph.set_stroke(YELLOW, 3)

        f_label, g_label = func_labels = VGroup(
            Tex("f(x)", font_size=36),
            Tex("g(y)", font_size=36)
        )
        for label, axes in zip(func_labels, all_axes):
            label.move_to(axes, UL)

        self.add(f_axes, f_graph, f_label)
        self.add(g_axes, g_graph, g_label)

        # Hook up trackers
        x_tracker = ValueTracker()
        y_tracker = ValueTracker()

        get_x = x_tracker.get_value
        get_y = y_tracker.get_value

        x_indicator, y_indicator = indicators = ArrowTip(90 * DEGREES).replicate(2)
        indicators.scale(0.5)
        indicators.set_fill(GREY_B)
        x_indicator.add_updater(lambda m: m.move_to(f_axes.c2p(get_x(), 0), UP))
        y_indicator.add_updater(lambda m: m.move_to(g_axes.c2p(get_y(), 0), UP))

        x_label, y_label = DecimalNumber(font_size=24).replicate(2)
        x_label.add_updater(lambda m: m.set_value(get_x()).next_to(x_indicator, DOWN, SMALL_BUFF).fix_in_frame())
        y_label.add_updater(lambda m: m.set_value(get_y()).next_to(y_indicator, DOWN, SMALL_BUFF).fix_in_frame())

        Axes.get_v_line_to_graph
        x_line = Line().set_stroke(WHITE, 1)
        y_line = Line().set_stroke(WHITE, 1)
        x_line.add_updater(lambda m: m.put_start_and_end_on(
            f_axes.c2p(get_x(), 0), f_axes.i2gp(get_x(), f_graph)
        ))
        y_line.add_updater(lambda m: m.put_start_and_end_on(
            g_axes.c2p(get_y(), 0), g_axes.i2gp(get_y(), g_graph)
        ))

        x_dot = GlowDot(color=BLUE)
        y_dot = GlowDot(color=YELLOW)
        x_dot.add_updater(lambda m: m.move_to(f_axes.i2gp(get_x(), f_graph)))
        y_dot.add_updater(lambda m: m.move_to(g_axes.i2gp(get_y(), g_graph)))

        # Ask about analog
        question = Text("What is analgous to this?")
        question.move_to(FRAME_WIDTH * RIGHT / 4)
        question.to_edge(UP)
        arrow = Vector(DOWN).next_to(question, DOWN)

        self.play(
            Write(question),
            GrowArrow(arrow),
            self.frame.animate.center().set_anim_args(run_time=2)
        )
        self.wait()

        # Scan over inputs
        x_tracker.set_value(-2)
        y_tracker.set_value(-2)
        self.add(x_indicator, x_label, x_line, x_dot)
        self.add(y_indicator, y_label, y_line, y_dot)
        self.play(LaggedStart(
            x_tracker.animate.set_value(0.31),
            y_tracker.animate.set_value(0.41),
            run_time=5,
            lag_ratio=0.2,
        ))
        self.wait()

        # Show the xy-plane
        plane = self.get_plane()
        plane.to_edge(RIGHT)

        x_indicator2 = x_indicator.copy().clear_updaters()
        y_indicator2 = y_indicator.copy().clear_updaters()
        y_indicator2.rotate(-90 * DEGREES)
        VGroup(x_indicator2, y_indicator2).scale(0.8)

        x_indicator2.add_updater(lambda m: m.move_to(plane.c2p(get_x()), UP))
        y_indicator2.add_updater(lambda m: m.move_to(plane.c2p(0, get_y()), RIGHT))

        self.play(
            FadeOut(question, UP),
            Uncreate(arrow),
            TransformFromCopy(f_axes.x_axis, plane.x_axis),
            TransformFromCopy(g_axes.x_axis, plane.y_axis),
            TransformFromCopy(x_indicator, x_indicator2),
            TransformFromCopy(y_indicator, y_indicator2),
            TransformFromCopy(f_axes[-1], plane.axis_labels[0]),
            TransformFromCopy(g_axes[-1], plane.axis_labels[1]),
        )
        self.play(
            Write(plane.background_lines, stroke_width=0.5, lag_ratio=0.01),
            Write(plane.faded_lines, stroke_width=0.5, lag_ratio=0.01),
        )
        self.add(plane, x_indicator2, y_indicator2)

        # Add plane lines
        h_line = Line().set_stroke(BLUE, 1)
        v_line = Line().set_stroke(YELLOW, 1)
        h_line.add_updater(lambda l: l.put_start_and_end_on(
            plane.c2p(0, get_y()), plane.c2p(get_x(), get_y())
        ))
        v_line.add_updater(lambda l: l.put_start_and_end_on(
            plane.c2p(get_x(), 0), plane.c2p(get_x(), get_y())
        ))

        dot = GlowDot(color=GREEN)
        dot.add_updater(lambda m: m.move_to(plane.c2p(get_x(), get_y())))
        xy_label = Tex("(x, y)", font_size=30)
        xy_label.add_updater(lambda m: m.next_to(dot, UR, buff=-SMALL_BUFF))

        self.play(LaggedStart(
            VFadeIn(h_line),
            VFadeIn(v_line),
            FadeIn(dot),
            VFadeIn(xy_label),
        ))
        self.wait()
        self.play(x_tracker.animate.set_value(1), run_time=2)
        self.play(y_tracker.animate.set_value(0.9), run_time=2)
        self.play(x_tracker.animate.set_value(0.2), run_time=2)
        self.wait()

        # Note probability density at a single point
        rect = SurroundingRectangle(xy_label, buff=0.05)
        rect.set_stroke(TEAL, 1)
        label = TexText("Probability density = $f(x)g(y)$", font_size=36)
        label.next_to(rect, UP)
        label.set_backstroke()

        prob_word = label["Probability"]
        equals = label["="]
        prob_word.save_state()
        prob_word.next_to(equals, LEFT)

        self.play(
            FadeIn(rect),
            FadeIn(prob_word, lag_ratio=0.1),
            FadeIn(equals),
        )
        self.wait()
        self.play(
            prob_word.animate.restore(),
            FadeIn(label["density"])
        )
        self.wait()

        self.play(LaggedStart(
            FadeTransform(f_label.copy(), label["f(x)"][0]),
            FadeTransform(g_label.copy(), label["g(y)"][0]),
            lag_ratio=0.3,
            run_time=2
        ))
        self.add(label)
        self.play(FadeOut(rect))
        self.wait()

        # Draw 3d graph
        to_fix = [
            f_axes, f_graph, f_label, x_indicator, x_label, x_line, x_dot,
            g_axes, g_graph, g_label, y_indicator, y_label, y_line, y_dot,
            label,
        ]
        for mobject in to_fix:
            mobject.fix_in_frame()
        plane.set_flat_stroke(False)

        three_d_axes = self.get_three_d_axes(plane)
        surface = three_d_axes.get_graph(
            lambda x, y: self.f(x) * self.g(y),
            resolution=self.graph_resolution,
        )

        self.play(
            FadeIn(surface),
            label.animate.set_x(FRAME_WIDTH / 4).to_edge(UP),
            self.frame.animate.reorient(-27, 78, 0).move_to([0.36, -0.62, 0.71]).set_height(5.66).set_anim_args(run_time=4),
        )
        surface.always_sort_to_camera(self.camera)
        self.play(
            self.frame.animate.reorient(68, 77, 0).move_to([-0.13, -1.12, -0.27]).set_height(9.37),
            run_time=5,
        )

        # Show two perspectives
        self.play(
            self.frame.animate.reorient(3, 83, 0).move_to([1.09, -0.82, -0.54]).set_height(6.91),
            run_time=4,
        )
        self.wait()
        self.play(
            self.frame.animate.reorient(89, 95, 0).move_to([0.63, -2.19, 2.56]).set_height(9.41),
            run_time=4,
        )
        self.wait()
        self.play(
            self.frame.animate.reorient(69, 75, 0).move_to([1.07, -1.37, -0.19]).set_height(7.64),
            run_time=5,
        )

    def get_plane(self):
        plane = NumberPlane(
            **self.plane_config,
            background_line_style=self.plane_line_style,
        )
        axis_labels = VGroup(
            Tex("x", font_size=24).next_to(plane.x_axis, RIGHT, SMALL_BUFF),
            Tex("y", font_size=24).next_to(plane.y_axis, UP, SMALL_BUFF),
        )
        axis_labels.insert_n_curves(100)
        axis_labels.make_jagged()
        plane.axis_labels = axis_labels
        plane.add(*axis_labels)
        return plane

    def get_three_d_axes(self, plane):
        axes = ThreeDAxes(
            plane.x_range,
            plane.y_range,
            (0, 1),
            width=plane.x_axis.get_width(),
            height=plane.y_axis.get_height(),
            depth=self.z_axis_height
        )
        axes.shift(plane.c2p(0, 0) - axes.c2p(0, 0, 0))
        axes.z_axis.apply_depth_test()
        return axes

    def f(self, x):
        return wedge_func(x)

    def g(self, y):
        return double_lump(y)


class DiagonalSlices(Introduce3DGraph):
    mesh_resolution = (21, 21)
    shadow_opacity = 0.25
    add_shadow = True
    shadow_bump = 0.01
    clip_plane_unit_coord = 0.45

    def setup(self):
        super().setup()
        plane, axes = self.add_plane_and_axes()
        self.s_tracker = ValueTracker(-2 * plane.x_range[1])
        get_s = self.s_tracker.get_value
        self.add_surface_group(axes, get_s)
        self.add_slice_graph(get_s)

        self.init_func_name()
        self.init_line_labels(get_s)

        self.add(self.func_name)

    def construct(self):
        # Get some nice local variables
        frame = self.camera.frame
        plane = self.plane
        axes = self.axes
        s_tracker = self.s_tracker
        slice_graph = self.slice_graph

        # Insert
        self.remove(self.equation)
        axes.z_axis.set_opacity(1)
        axes.z_axis.set_flat_stroke(True)
        frame.reorient(80, 70).move_to(ORIGIN),
        s_tracker.set_value(-5)
        self.play(
            frame.animate.reorient(40, 70).move_to(ORIGIN),
            run_time=20,
        )

        # Initial orientation
        self.frame.reorient(88, 90, 0).move_to([-0.31, -2.14, 2.16])
        self.play(frame.animate.reorient(40, 70).move_to(ORIGIN), run_time=10)
        self.play(
            s_tracker.animate.set_value(0.5),
            frame.animate.reorient(0, 0),
            VFadeIn(self.equation),
            FadeOut(axes.z_axis),
            run_time=6,
        )
        self.wait()

        # Show x + y = s slice
        self.play(
            FadeIn(self.ses_label, 0.5 * DOWN),
            MoveAlongPath(GlowDot(), slice_graph, run_time=5, remover=True)
        )
        self.wait()
        self.play(
            self.frame.animate.reorient(-22, 74, 0).move_to([-0.12, -0.16, 0.04]).set_height(5.45),
            run_time=3
        )
        self.wait()

        # Change s
        self.play(
            s_tracker.animate.set_value(1.5),
            self.frame.animate.reorient(-45, 75, 0).move_to([0.18, -0.14, 0.49]).set_height(3.0),
            run_time=6,
        )
        self.play(
            s_tracker.animate.set_value(-2.0),
            self.frame.animate.reorient(-5, 66, 0).move_to([-0.03, -0.18, 0.14]).set_height(6.35),
            run_time=20,
        )
        self.play(
            s_tracker.animate.set_value(2.0),
            self.frame.animate.reorient(16, 73, 0).move_to([-0.03, -0.18, 0.14]).set_height(6.35),
            run_time=15,
        )

    def add_plane_and_axes(self):
        frame = self.camera.frame
        frame.reorient(20, 70)
        plane = self.plane = self.get_plane()
        plane.axes.set_stroke(GREY_B)
        plane.set_flat_stroke(False)
        plane.remove(plane.faded_lines)
        axes = self.axes = self.get_three_d_axes(plane)

        self.add(axes, axes.z_axis)
        self.add(plane)

        self.plane = plane
        self.axes = axes

        return plane, axes

    def add_surface_group(self, axes, get_s):
        # Surface
        surface = axes.get_graph(
            lambda x, y: self.f(x) * self.g(y),
            resolution=self.graph_resolution
        )
        vect = axes.c2p(*2 * [self.clip_plane_unit_coord], 0)  # Why?
        surface.add_updater(lambda m: m.set_clip_plane(vect, -get_s()))
        surface.always_sort_to_camera(self.camera)

        surface_mesh = SurfaceMesh(surface, resolution=self.mesh_resolution)
        surface_mesh.set_stroke(WHITE, width=1, opacity=0.1)

        surface_group = Group(surface, surface_mesh)

        # Add shadow
        if self.add_shadow:
            surface_shadow = surface.copy()
            surface_shadow.set_opacity(self.shadow_opacity)
            surface_shadow.shift(self.shadow_bump * IN)
            self.add(surface_shadow)

            surface_group.add(surface_shadow)

        self.surface_group = surface_group
        self.add(surface_group)
        return surface_group

    def add_slice_graph(
        self, get_s,
        stroke_color=WHITE,
        stroke_width=2,
        fill_color=TEAL_D,
        fill_opacity=0.5,
        dx=0.01
    ):
        axes = self.axes

        def get_points(s):
            x_min, x_max = axes.x_range[:2]
            y_min, y_max = axes.y_range[:2]

            if s > 0:
                xs = np.arange(s - y_max, x_max, dx)
            else:
                xs = np.arange(x_min, s - y_min, dx)

            return axes.c2p(xs, s - xs, self.f(xs) * self.g(s - xs))

        graph = VMobject()
        graph.set_flat_stroke(False)
        graph.set_stroke(stroke_color, stroke_width)
        graph.set_fill(fill_color, fill_opacity)
        graph.add_updater(lambda m: m.set_points_as_corners(get_points(get_s())))

        self.add(graph)
        self.slice_graph = graph

    def init_func_name(self):
        self.func_name = Tex(
            R"f(x) \cdot g(y)",
            font_size=42,
        )
        self.func_name.to_corner(UL, buff=0.25)
        self.func_name.fix_in_frame()
        return self.func_name

    def init_line_labels(self, get_s):
        equation = Tex("x + y = 0.00")
        s_label = equation.make_number_changeable("0.00")
        s_label.add_updater(lambda m: m.set_value(get_s()))
        equation.to_corner(UR)
        equation.fix_in_frame()

        ses_label = Tex(R"\{(x, s - x): x \in \mathds{R}\}", tex_to_color_map={"s": YELLOW}, font_size=30)
        ses_label.next_to(equation, DOWN, MED_LARGE_BUFF, aligned_edge=RIGHT)
        ses_label.fix_in_frame()

        self.equation = equation
        self.ses_label = ses_label

        return equation, ses_label


class RotationalSymmetryOfGaussian(DiagonalSlices):
    plane_config = dict(
        x_range=(-3, 3),
        y_range=(-3, 3),
        width=8.0,
        height=8.0,
    )
    mesh_resolution = (25, 25)
    clip_plane_unit_coord = 0.565

    def construct(self):
        # Variables
        frame = self.frame
        axes = self.axes
        s_tracker = self.s_tracker
        surface_group = self.surface_group
        slice_graph = self.slice_graph

        # Add functions
        self.add_function_labels()

        # Show slices
        s_tracker.set_value(1)
        frame.reorient(-20, 69, 0).move_to(0.5 * OUT)
        self.play(
            frame.animate.reorient(20, 69, 0),
            s_tracker.animate.set_value(-6),
            run_time=8
        )

        # Emphasize rotational symmetry
        curve = VMobject()
        curve.set_stroke(TEAL, 3)
        dx = 0.05
        xs = np.arange(*axes.x_range, dx)
        curve.set_points_smoothly(axes.c2p(xs, np.zeros(xs.size), self.f(xs)))
        curve.set_flat_stroke(False)
        curve.make_jagged()
        curve.apply_depth_test()
        curve.shift(0.025 * OUT)
        curves = VGroup(*(
            curve.copy().rotate(a, about_point=axes.c2p(0, 0, 0))
            for a in np.linspace(0, PI, 25)
        ))
        curves.set_stroke(width=1, opacity=0.5)

        self.play(ShowCreation(curve))
        self.play(
            Rotate(curve, PI, about_point=ORIGIN),
            ShowIncreasingSubsets(curves, rate_func=smooth),
            self.frame.animate.reorient(-20, 69, 0).center(),
            Rotate(surface_group, PI),
            run_time=7
        )
        self.play(
            FadeOut(curve, time_span=(0, 2)),
            FadeOut(curves, time_span=(0, 2)),
        )
        self.wait()

        # Show r
        surface, mesh, ghost_surface = surface_group
        surface_group.generate_target()
        surface_group.target[0].set_opacity(0.25)

        self.play(
            MoveToTarget(surface_group),
            frame.animate.reorient(0, 0).set_height(10).move_to(1.5 * LEFT).set_field_of_view(1 * DEGREES),
            FadeOut(self.func_names),
            run_time=4,
        )
        self.wait()

        # Explain meaning of r
        x, y = (1.5, 0.75)
        dot = Dot(axes.c2p(x, y), fill_color=RED)
        dot.set_stroke(WHITE, 0.5)
        coords = Tex("(x, y)", font_size=36)
        coords.set_backstroke(width=5)
        coords.next_to(dot, UR, SMALL_BUFF)
        coords.shift(0.1 * DOWN)

        x_line = Line(axes.get_origin(), axes.c2p(x, 0, 0))
        y_line = Line(axes.c2p(x, 0, 0), axes.c2p(x, y, 0))
        r_line = Line(axes.c2p(x, y, 0), axes.get_origin())
        x_line.set_stroke(BLUE, 3)
        y_line.set_stroke(YELLOW, 3)
        r_line.set_stroke(RED, 3)
        lines = VGroup(x_line, y_line, r_line)
        labels = VGroup(*map(Tex, "xyr"))
        for label, line in zip(labels, lines):
            label.match_color(line)
            label.scale(0.85)
            label.next_to(line.get_center(), rotate_vector(line.get_vector(), -90 * DEGREES), SMALL_BUFF)

        self.add(dot, coords)
        self.play(
            FadeIn(dot, scale=0.5),
            FadeIn(coords),
        )
        for line, label in zip(lines, labels):
            self.add(line, label, dot)
            self.play(
                ShowCreation(line),
                Write(label),
            )

    def add_function_labels(self):
        kw = dict(t2c={"x": BLUE, "y": YELLOW})
        func_names = VGroup(
            Tex("f(x) = e^{-x^2}", **kw),
            Tex("g(y) = e^{-y^2}", **kw),
        )
        func_names.scale(0.75)
        func_names.arrange(DOWN, buff=MED_LARGE_BUFF)
        func_names.to_corner(UL)
        func_names.fix_in_frame()
        self.func_names = func_names

        self.remove(self.func_name)
        self.add(func_names)

    def f(self, x):
        return np.exp(-x**2)

    def g(self, x):
        return np.exp(-x**2)


class Thumbnail(RotationalSymmetryOfGaussian):
    def construct(self):
        # Variables
        frame = self.frame
        axes = self.axes
        s_tracker = self.s_tracker
        surface_group = self.surface_group
        slice_graph = self.slice_graph
        self.add(s_tracker)
        self.remove(self.func_name)
        self.remove(self.equation)
        s_tracker.set_value(0)
        frame.reorient(0, 47, 0)

        # Better surface
        surface, mesh, shadow = surface_group
        shadow.clear_updaters()
        shadow.set_clip_plane(ORIGIN, 00)
        shadow.set_opacity(0.5)

        self.add(shadow, surface, mesh, slice_graph)

        # Title
        title = TexText("It's about symmetry", font_size=90)
        title.to_edge(UP)
        title.fix_in_frame()
        self.add(title)
