# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2023/clt/main.py (lines 3499-3560)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING

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
