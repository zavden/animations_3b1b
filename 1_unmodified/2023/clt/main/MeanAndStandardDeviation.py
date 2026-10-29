# ==============================================================================
# Scene:      MeanAndStandardDeviation
# Source:     videos/_2023/clt/main.py (lines 1152-1470)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MeanAndStandardDeviation.py MeanAndStandardDeviation -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Sequence
    from manimlib.typing import ManimColor


EXP_DISTRIBUTION = [0.41, 0.25, 0.15, 0.10, 0.06, 0.03]


U_SHAPED_DISTRIBUTION = [0.3, 0.15, 0.05, 0.05, 0.15, 0.3]


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


def get_die_distribution_chart(
    dist: list[float],
    die_config=dict(),
    axes_config=dict(
        width=4,
        height=3,
    ),
    font_size=25,
    y_range=(0, 1, 0.2),
    max_value: int = 6,
    bar_colors=(BLUE, TEAL)
):
    axes = Axes((0, max_value), y_range, **axes_config)
    ndp = len(str(y_range[2])) - 2
    axes.y_axis.add_numbers(font_size=font_size, num_decimal_places=ndp)
    bars = ChartBars(axes, dist)
    bars.set_submobject_colors_by_gradient(*bar_colors)

    dice = VGroup()
    for n in range(1, max_value + 1):
        die = DieFace(n, **die_config)
        die.set_width(0.5 * axes.x_axis.get_unit_size())
        die.next_to(axes.c2p(n - 0.5, 0), DOWN, SMALL_BUFF)
        dice.add(die)

    result = VGroup(axes, bars, dice)
    result.axes = axes
    result.bars = bars
    result.dice = dice
    return result


class MeanAndStandardDeviation(InteractiveScene):
    def construct(self):
        # Setup axes
        dist = np.array([3, 2, 1, 0.5, 1, 0.75])
        dist /= dist.sum()
        original_dist = dist

        die_config = dict(
            fill_color=BLUE_E,
            dot_color=WHITE,
        )
        chart = get_die_distribution_chart(
            dist,
            y_range=(0, 0.5, 0.1),
            die_config=die_config
        )
        chart.to_edge(LEFT)
        self.add(*chart)

        axes, bars, die_labels = chart
        assert(isinstance(axes, Axes))

        # Functions
        def set_dist(dist, **kwargs):
            new_bars = ChartBars(axes, dist)
            new_bars.match_style(bars)
            self.play(Transform(bars, new_bars, **kwargs))

        def get_dist():
            result = np.array([bar.get_height() for bar in bars])
            return result / result.sum()

        def get_mu():
            dist = get_dist()
            return sum(p * (n + 1) for n, p in enumerate(dist))

        def get_sigma():
            dist = get_dist()
            mu = get_mu()
            return math.sqrt(sum(p * (n + 1 - mu)**2 for n, p in enumerate(dist)))

        # Mean line
        tex_kw = dict(
            t2c={R"\mu": PINK, R"\sigma": RED},
            font_size=48
        )

        mean_line = Line(axes.c2p(0, 0), axes.c2p(0, 0.5))
        mean_line.set_stroke(PINK, 3)
        mean_line.add_updater(lambda m: m.move_to(axes.c2p(get_mu() - 0.5, 0), DOWN))
        mu_label = Tex(R"\mu = 1.00", **tex_kw)
        mu_number = mu_label.make_number_changeable("1.00")
        mu_number.add_updater(lambda m: m.set_value(get_mu()))
        mu_number.scale(0.75, about_edge=LEFT)
        mu_label.add_updater(lambda m: m.next_to(mean_line, UP))

        mean_name = Text("Mean")
        mean_name.next_to(mu_label, UL, buff=1.0)
        mean_name.shift_onto_screen()
        mean_arrow = Arrow(mean_name, mu_label)
        mean_arrow.add_updater(lambda m: m.put_start_and_end_on(
            mean_name.get_bottom(), mu_label.get_corner(UL)
        ).scale(0.7))

        self.play(
            ShowCreation(mean_line),
            VFadeIn(mu_label),
        )
        self.wait()
        self.play(
            ShowCreation(mean_arrow),
            FadeIn(mean_name, 0.5 * UL)
        )

        # Show a few means
        dists = [
            EXP_DISTRIBUTION[::-1],
            EXP_DISTRIBUTION,
            U_SHAPED_DISTRIBUTION,
            original_dist
        ]
        for dist in dists:
            set_dist(dist, run_time=2)
            self.wait()

        # Mean equation
        mean_eq = Tex(R"\mu = E[X] = \sum_{x} P(X = x) \cdot x =", **tex_kw)
        mean_eq[R"\mu"].scale(1.2, about_edge=RIGHT)
        rhs = VGroup()
        for n in range(1, 7):
            term = Tex(Rf"P(\square) \cdot {n} \, + ", **tex_kw)
            die = DieFace(n, **die_config)
            die.replace(term[R"\square"])
            term.replace_submobject(2, die)
            term.add(die)
            rhs.add(term)

        rhs.arrange(DOWN, buff=0.35)
        rhs[-1][-1].set_opacity(0)
        rhs.scale(0.75)
        mean_eq.next_to(rhs[0], LEFT, submobject_to_align=mean_eq[-1])
        VGroup(mean_eq, rhs).to_corner(UR)

        mean_eq[-1].set_opacity(0)
        self.play(Write(mean_eq))
        self.wait()

        # Highlight terms
        highlights = chart.bars.copy()
        highlights.set_stroke(YELLOW, 3)
        highlights.set_fill(opacity=0)

        for highlight, die, part in zip(highlights, chart.dice, rhs):
            self.play(
                ShowCreation(highlight),
                mean_eq[-1].animate.set_opacity(1),
            )
            self.play(
                TransformMatchingShapes(die.copy(), part),
                FadeOut(highlight),
                run_time=1
            )

        # Show a few other distributions again
        for dist in dists:
            set_dist(dist, run_time=2)
            self.wait()

        # Reorganize mean labels
        mu_label.target = mu_label.generate_target()
        mu_label.target[1:].scale(0, about_point=mu_label[0].get_right())
        mu_label.target.match_x(mean_line)
        mu_number.clear_updaters()
        self.play(
            MoveToTarget(mu_label),
            LaggedStart(
                FadeOut(mean_name),
                FadeOut(mean_arrow),
                FadeOut(rhs),
                FadeOut(mean_eq[-1]),
            )
        )
        mu_label.remove(*mu_label[1:])

        # Standard deviation
        sd_lines = mean_line.copy().replicate(2)
        sd_lines.set_stroke(RED, 3)
        sd_lines.clear_updaters()
        sd_lines[0].add_updater(lambda m: m.move_to(
            axes.c2p(get_mu() - get_sigma() - 0.5, 0), DOWN)
        )
        sd_lines[1].add_updater(lambda m: m.move_to(
            axes.c2p(get_mu() + get_sigma() - 0.5, 0), DOWN)
        )
        sd_arrows = VGroup(Vector(LEFT), Vector(RIGHT))
        sd_arrows.set_color(RED)
        sd_arrows.arrange(RIGHT, buff=0.35)
        sd_arrows.add_updater(lambda m: m.set_width(0.8 * sd_lines.get_width()))
        sd_arrows.add_updater(lambda m: m.move_to(sd_lines).shift(UP))

        sd_lines.save_state()
        sd_lines.stretch(0.5, 0).set_opacity(0)

        self.play(
            Restore(sd_lines),
            ShowCreation(sd_arrows, lag_ratio=0),
        )
        self.wait()

        # Contrast low and high variance
        var_dists = [
            np.array([1, 3, 12, 4, 2, 1], dtype='float'),
            np.array([10, 2, 1, 1, 2, 10], dtype='float'),
        ]

        for dist in var_dists:
            dist /= dist.sum()
            set_dist(dist, run_time=3)
            self.wait()

        # Variance equation
        var_eq = VGroup(
            Tex(R"\text{Var}(X) &= E[(X - \mu)^2]", **tex_kw),
            Tex(R"= \sum_x P(X = x) \cdot (x - \mu)^2", **tex_kw),
        )
        var_eq[1].next_to(var_eq[0]["="], DOWN, LARGE_BUFF, aligned_edge=LEFT)

        var_eq.next_to(mean_eq["E[X]"], DOWN, buff=1.5, aligned_edge=LEFT)

        variance_name = Text("Variance")
        variance_name.next_to(var_eq[0]["Var"], DOWN, buff=1.25).shift(0.5 * LEFT)
        variance_name.set_color(YELLOW)
        variance_arrow = Arrow(variance_name, var_eq[0]["Var"])
        variance_arrow.match_color(variance_name)

        self.play(
            FadeIn(var_eq[0], DOWN),
            mean_eq.animate.set_opacity(0.5),
        )
        self.play(
            Write(variance_name),
            ShowCreation(variance_arrow)
        )
        self.wait()
        self.play(Write(var_eq[1]))
        self.wait()

        partial_square_opacity_tracker = ValueTracker(0)

        # Show squares
        partial_square_opacity_tracker.set_value(0.5)
        new_dist = np.array([10, 2, 1, 3, 4, 13], dtype='float')
        new_dist /= new_dist.sum()
        sd_group = VGroup(sd_lines, sd_arrows)

        def get_squares(bars):
            result = VGroup()
            for bar in bars:
                prob = axes.y_axis.p2n(bars[0].get_top())
                line = Line(bar.get_bottom(), mean_line.get_bottom())
                square = Square(line.get_width())
                square.move_to(line, DOWN)
                square.match_y(bar.get_top(), DOWN)
                square.set_stroke(RED, 1)
                square.set_fill(RED, 0.2)
                p_square = square.copy()
                p_square.stretch(prob, 1, about_edge=DOWN)
                p_square.set_opacity(partial_square_opacity_tracker.get_value())
                result.add(VGroup(square, p_square))
            return result

        squares = get_squares(bars)
        labels = VGroup(*(Tex(Rf"P({n}) \cdot ({n} - \mu)^2", **tex_kw) for n in range(1, 7)))
        labels.scale(0.5)
        for label, square in zip(labels, squares):
            label.square = square
            label.add_updater(lambda m: m.set_width(0.7 * m.square.get_width()).next_to(m.square.get_bottom(), UP, SMALL_BUFF))

        label = labels[0]
        square = squares[0]
        square[1].set_fill(opacity=0)
        part1 = label[R"P(1) \cdot"]
        part2 = label[R"(1 - \mu)^2"]
        part2.save_state()
        part2.match_x(squares[0])
        self.play(
            FadeOut(sd_group),
            FadeIn(square, lag_ratio=0.8),
            FadeIn(part2),
        )
        self.wait()
        self.play(
            square[1].animate.set_fill(opacity=0.5),
            FadeIn(part1),
            Restore(part2),
        )
        self.add(label)

        # Show other squares
        last_group = VGroup(square, label)
        for new_label, new_square in zip(labels[1:], squares[1:]):
            new_group = VGroup(new_square, new_label)
            self.play(FadeOut(last_group), FadeIn(new_group))
            last_group = new_group
        self.play(
            FadeOut(last_group),
            FadeIn(square), FadeIn(label),
        )
        self.wait()

        squares = always_redraw(lambda: get_squares(bars[:1]))
        self.remove(square)
        self.add(squares, label)

        # Again, toggle between low and  high variance
        for dist in [var_dists[0], EXP_DISTRIBUTION, var_dists[1]]:
            set_dist(dist, run_time=3)
            self.wait(2)

        sd_group.update()
        self.play(FadeOut(squares), FadeOut(label), FadeIn(sd_group))
        self.wait()

        # Standard deviation
        sd_equation = Tex(R"\sigma = \sqrt{\text{Var}(X)}", **tex_kw)
        sd_equation.next_to(var_eq, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        sd_name = Text("Standard deviation")
        sd_name.set_color(RED)
        sd_name.next_to(sd_equation, DOWN, LARGE_BUFF).shift_onto_screen()
        sd_name.shift(2 * LEFT)
        sd_arrow = Arrow(sd_name, sd_equation[R"\sigma"], buff=0.1)
        sd_arrow.match_color(sd_name)

        sigma_labels = Tex(R"\sigma", **tex_kw).replicate(2)
        for label, arrow in zip(sigma_labels, sd_arrows):
            label.arrow = arrow
            label.add_updater(lambda m: m.next_to(m.arrow, UP))

        self.play(
            FadeTransformPieces(variance_name, sd_name),
            ReplacementTransform(variance_arrow, sd_arrow),
            Write(sd_equation[:-len("Var(X)")]),
            TransformFromCopy(
                var_eq[0][R"\text{Var}(X)"],
                sd_equation[R"\text{Var}(X)"],
            ),
        )
        self.wait()
        self.play(*(
            TransformFromCopy(sd_equation[R"\sigma"][0], label)
            for label in sigma_labels
        ))
        self.wait()

        # Show a few distributions
        for dist in [*dists, *var_dists]:
            set_dist(dist, run_time=2)
            self.wait()
