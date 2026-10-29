# ==============================================================================
# Scene:      UDistSumDistributions
# Source:     videos/_2023/clt/main.py (lines 1146-1147)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UDistSumDistributions.py UDistSumDistributions -w -m --fps 15
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


def get_sample_markers(bars, samples):
    width = 0.25 * bars[0].get_width()
    tips = ArrowTip(angle=-90 * DEGREES).replicate(len(samples))
    tips.set_width(width)
    tips.set_height(0.5 * width, stretch=True)
    tips.set_fill(YELLOW, 1)
    tip_map = [VGroup() for b in bars]
    for sample, tip in zip(samples, tips):
        tip_map[sample - 1].add(tip)

    for value, group in enumerate(tip_map):
        group.arrange(UP, buff=0.5 * width)
        group.next_to(bars[value], UP, SMALL_BUFF)

    return tips


class DiceSumDistributions(InteractiveScene):
    distribution = [1 / 6] * 6
    max_plot_width = 10
    n_examples = 7
    values = list(range(1, 7))

    def construct(self):
        # Setup all plots
        plots = VGroup(*(
            self.get_sum_distribution_plot(
                n,
                y_max=(0.2 if n > 1 else 0.5)
            )
            for n in range(1, self.n_examples + 1)
        ))
        plots.scale(0.9)
        plots.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        plots.to_corner(UL)

        labels = VGroup(*(
            self.get_plot_label(plot, n, die_face=True)
            for plot, n in zip(plots, it.count(1))
        ))

        # n = 1 distribution
        plot1 = plots[0]
        plot1.save_state()
        plot1.set_height(4)
        plot1.center()

        dice = self.get_dice_axis_labels(plot1)

        axes, bars = plot1

        prob_labels = Tex(r"1 / 6").replicate(6)
        for label, bar in zip(prob_labels, bars):
            label.set_width(0.5 * bar.get_width())
            label.next_to(bar, UP)

        self.add(plot1, dice)
        self.play(Write(prob_labels))
        self.wait()

        axes.add(dice, prob_labels)
        plot1.generate_target()
        plot1.target.replace(plot1.saved_state)

        # Grid of dice to bar chart
        grid = Square().get_grid(6, 6, buff=0)
        grid.set_stroke(GREY, 2)
        grid.set_height(5.5)
        grid.to_corner(UR)

        plot2 = plots[1]
        axes, bars = plot2
        plot2.save_state()
        plot2.set_width(10)
        plot2.center().to_edge(DOWN)
        axes.y_axis.numbers.set_opacity(0)

        die_groups = [VGroup() for n in range(6)]
        columns = VGroup(*(VGroup() for n in range(11)))
        for n, square in enumerate(grid):
            i = n % 6
            j = n // 6
            die1 = dice[i].copy()
            die2 = dice[j].copy()
            die2.set_fill(RED_E)
            die2.dots.set_fill(WHITE)
            pair = VGroup(die1, die2)
            pair.arrange(RIGHT, buff=SMALL_BUFF)
            pair.move_to(square)
            square.dice = pair
            columns[i + j].add(square)
            die_groups[i].add(die1)
            die_groups[j].add(die2)

        self.play(
            MoveToTarget(plot1),
            LaggedStart(*(
                TransformFromCopy(VGroup(dice[n]), die_groups[n])
                for n in range(6)
            ), lag_ratio=0.1),
            Write(grid),
            run_time=3
        )
        self.wait()

        for square in grid:
            square.add(square.dice)

        column_targets = VGroup()
        for column in columns:
            column.target = column.generate_target()
            for square in column.target:
                square.stretch(0.5, 1)
                square.dice.stretch(2, 1)
            column.target.arrange(DOWN, buff=0)
            column_targets.add(column.target)
        column_targets.arrange(RIGHT, buff=0, aligned_edge=DOWN)
        column_targets.match_width(bars[1:])
        column_targets.move_to(bars[1:], DOWN)

        bars.match_height(column_targets, stretch=True, about_edge=DOWN)
        bars.set_opacity(0.25)

        axes = plot2[0]
        axes.save_state()
        axes.set_opacity(0)
        self.add(axes)
        for column in columns:
            ct = column.target
            self.play(column.animate.set_stroke(YELLOW, 2))
            self.play(
                Transform(column, ct, run_time=1, lag_ratio=0.001),
                Restore(axes),
            )
        self.add(plot2[1], columns)
        self.play(FadeIn(plot2[1]))
        self.add(plot2, columns)
        self.wait()

        # n = 2 prob labels
        prob_labels = VGroup()
        for column in columns:
            label = Tex("1 / 36")
            numer = label.make_number_changeable("1")
            numer.edge_to_fix = RIGHT
            numer.set_value(len(column))
            label.next_to(column, UP, SMALL_BUFF)
            label.set_width(0.6 * column.get_width())
            prob_labels.add(label)

        self.play(Write(prob_labels))
        self.wait()
        labelled_bars = VGroup(bars, columns, prob_labels)
        labelled_bars.save_state()
        highlights = [
            VGroup(columns[n - 2], prob_labels[n - 2]).copy()
            for n in [6, 10]
        ]
        last = VMobject()
        for highlight in highlights:
            self.play(
                FadeOut(last),
                FadeIn(highlight),
                labelled_bars.animate.set_opacity(0.075)
            )
            last = highlight
            self.wait()
        self.play(
            FadeOut(last),
            Restore(labelled_bars),
        )

        # Restore
        columns.generate_target()
        pre_bars = plot2.saved_state[1][1:]
        columns.target.replace(pre_bars, stretch=True)
        columns.target.set_opacity(0)
        prob_labels.target = prob_labels.generate_target()
        for bar, label in zip(pre_bars, prob_labels.target):
            label.set_width(0.6 * bar.get_width())
            label.next_to(bar, UP, 0.5 * SMALL_BUFF)

        self.play(
            Restore(plot2),
            MoveToTarget(columns, remover=True),
            MoveToTarget(prob_labels),
            FadeIn(labels[:2], lag_ratio=0.2),
        )
        axes.add(prob_labels)
        self.wait()

        # Pan through the rest
        frame = self.frame
        frame.target = frame.generate_target()
        for n in range(1, len(plots) - 1):
            frame.target.match_y(plots[n])
            min_width = VGroup(plots[n + 1], labels[n + 1]).get_width() + 1
            frame.target.set_width(
                max(FRAME_WIDTH, min_width),
                about_edge=LEFT
            )
            self.play(LaggedStart(
                MoveToTarget(frame, run_time=2),
                FadeTransform(
                    plots[n].copy().set_opacity(0),
                    plots[n + 1], run_time=2
                ),
                TransformMatchingShapes(labels[n].copy(), labels[n + 1]),
                lag_ratio=0.2
            ))
            self.wait()

        frame.target.set_height(FRAME_HEIGHT)
        frame.target.center()
        frame.target.set_height(plots.get_height() + 1, about_edge=UL)
        self.play(MoveToTarget(frame, run_time=2))

        # Flash through
        plot_groups = VGroup(*(
            VGroup(plot, label)
            for plot, label in zip(plots, labels)
        ))
        for pg in plot_groups:
            pg.save_state()

        for pg1 in plot_groups:
            anims = []
            for pg2 in plot_groups:
                if pg2 is pg1:
                    anims.append(Restore(pg2))
                else:
                    anims.append(pg2.animate.restore().fade(0.85))
            self.play(*anims)
        self.play(LaggedStartMap(Restore, plot_groups))

        # Comment on center of mass straying to the right?
        mean_labels = self.get_mean_labels(plots)

        self.play(frame.animate.set_height(4).move_to(plots[0], DOWN).shift(DOWN))
        self.play(Write(mean_labels[0], run_time=1))
        self.wait()

        prob_labels.set_opacity(0)
        for n in range(6):
            frame.target = frame.generate_target()
            frame.target.set_height(plots[:n + 2].get_height() + 2)
            frame.target.move_to(plots[n + 1], DL).shift(0.75 * DL)

            self.play(LaggedStart(
                MoveToTarget(frame),
                TransformFromCopy(*mean_labels[n:n + 2]),
                lag_ratio=0.5
            ))
            self.wait()

        # Comment on distributions becoming more spread out?
        sd_labels = self.get_sd_labels(plots)
        for label in sd_labels:
            label.save_state()
            label.stretch(0, 0)
            label.set_opacity(0)

        self.play(
            LaggedStartMap(Restore, sd_labels),
            LaggedStart(*(
                FadeOut(label[1])
                for label in mean_labels
            )),
            run_time=3
        )
        self.wait()
        self.play(*(
            FadeOut(label[2])
            for label in sd_labels
        ))
        self.wait()

        mean_lines = VGroup(*(ml[0] for ml in mean_labels))
        sd_lines = VGroup(*(sl[:2] for sl in sd_labels))
        self.add(mean_lines, sd_lines)

        # Realign
        all_axes = VGroup(*(plot[0] for plot in plots))
        all_bars = VGroup(*(plot[1] for plot in plots))

        self.play(FadeOut(all_axes))
        self.realign_distributions(all_bars, labels, mean_lines, sd_lines)
        self.wait()

        # Rescale
        self.rescale_distributions(all_bars, mean_lines, sd_lines)

        # Draw up against normal curve
        axes = Axes(
            (-3, 3), (0, 1, 0.25),
            width=0.45 * frame.get_width(),
            height=0.18 * frame.get_height(),
        )
        axes.next_to(frame.get_left(), RIGHT, buff=1)
        axes.x_axis.add_numbers()
        axes.y_axis.add_numbers(np.arange(0.25, 1.25, 0.25), num_decimal_places=2)
        graph = axes.get_graph(lambda x: np.exp(-x**2))
        graph.set_stroke(YELLOW, 3)

        graph_label = Tex(R"e^{-x^2}")
        graph_label.set_height(0.5 * graph.get_height())
        graph_label.move_to(graph, UL)

        self.play(
            labels.animate.shift(1.5 * RIGHT),
            all_bars.animate.shift(4.5 * RIGHT),
            FadeOut(mean_lines, 4.5 * RIGHT),
            FadeOut(sd_lines, 4.5 * RIGHT),
            FadeIn(axes),
            ShowCreation(graph, run_time=2),
            Write(graph_label)
        )
        self.wait()

        # Rescale normal curve
        alt_graph_label = Tex(R"{1 \over \sigma \sqrt{2 \pi}} e^{-x^2 / 2\sigma^2}")
        alt_graph_label[R"{1 \over \sigma \sqrt{2 \pi}}"].scale(0.75, about_edge=RIGHT)
        alt_graph_label.set_height(1.25 * graph_label.get_height())
        alt_graph_label.move_to(graph_label, DL)
        mu, sigma = self.get_mean_and_standard_deviation(self.distribution)
        alt_graph = axes.get_graph(
            lambda x: (1 / sigma / math.sqrt(2 * PI)) * math.exp(-x**2 / 2 * sigma**2)
        )
        alt_graph.match_style(graph)
        self.play(
            Transform(graph, alt_graph),
            TransformMatchingTex(graph_label, alt_graph_label),
            run_time=2
        )
        axes.generate_target()
        sf = 3.5
        axes.target.y_axis.stretch(sf, 1, about_edge=DOWN)
        for number in axes.target.y_axis.numbers:
            number.stretch(1 / sf, 1)
        self.play(
            MoveToTarget(axes),
            graph.animate.stretch(sf, 1, about_edge=DOWN),
        )
        self.wait()

        # Map bell curve over bars
        graph_copies = VGroup(*(
            graph.copy().replace(
                bars[n:],
                dim_to_match=1
            ).set_stroke(width=1.5)
            for n, bars in zip(it.count(1), all_bars[1:])
        ))
        self.play(
            LaggedStart(*(
                TransformFromCopy(graph, graph_copy)
                for graph_copy in graph_copies
            )),
            run_time=3
        )
        self.wait()

    def get_plot_label(self, plot, n, die_face=False, height=0.35):
        # Test
        if die_face:
            die = DieFace(1).set_width(height)
            die.set_fill(BLUE_E)
            die.remove(*die.dots)
            terms = die.replicate(min(n, 5))
        else:
            term = Tex("X_0")
            term.make_number_changeable("0")
            terms = term.replicate(min(n, 5))
            for i, term in enumerate(terms):
                term[1].set_value(i + 1)


        if n > 5:
            terms.replace_submobject(2, Tex(R"\cdots"))
            if not die_face:
                terms[-2][1].set_value(n - 1)
                terms[-1][1].set_value(n)

        label = VGroup()
        for term in terms[:-1]:
            label.add(term)
            label.add(Tex("+"))
        label.add(terms[-1])
        label.arrange(RIGHT, buff=SMALL_BUFF)

        if n > 5 and die_face:
            brace = Brace(label, DOWN, SMALL_BUFF)
            count = brace.get_text(str(n), buff=SMALL_BUFF)
            label.add(brace, count)

        label.move_to(plot.get_corner(UR), UL)

        return label

    def get_sum_distribution_plot(self, n, **kwargs):
        return self.get_distribution_plot(
            self.get_sum_distribution(n),
            **kwargs
        )

    def get_distribution_plot(
        self,
        distribution,
        x_unit=0.5,
        height=1.5,
        bar_colors=(BLUE, TEAL),
        y_max=None,
    ):
        n = len(distribution)
        if y_max is not None:
            y_step = 0.1
        elif n == len(self.distribution):
            y_max = 0.5
            y_step = 0.1
        else:
            y_max = 0.05 * int(20 * max(distribution) + 2)
            y_step = 0.1 if y_max > 0.2 else 0.05

        axes = Axes(
            (0, n), (0, y_max, y_step),
            width=n * x_unit,
            height=height
        )
        axes.set_stroke(width=1)
        axes.center()
        axes.y_axis.add_numbers(
            num_decimal_places=len(str(y_step)) - 2,
            font_size=16
        )
        axes.x_axis.add_numbers(
            range(1, n + 1),
            num_decimal_places=0,
            font_size=int(axes.x_axis.get_unit_size() * 40),
            buff=0.1
        )
        axes.x_axis.numbers.shift(0.5 * axes.x_axis.get_unit_size() * LEFT)
        bars = ChartBars(axes, distribution)
        bars.set_submobject_colors_by_gradient(*bar_colors)
        bars.set_stroke(WHITE, 1)

        plot = VGroup(axes, bars)
        return plot

    def get_sum_distribution(self, n):
        dist0 = [0, *self.distribution]
        dist = np.array(dist0)
        for _ in range(n - 1):
            dist = np.convolve(dist, dist0)
        return dist[1:]

    def get_dice_axis_labels(self, plot):
        axes, bars = plot
        numbers = axes.x_axis.numbers
        die_faces = VGroup(*(
            DieFace(
                n + 1,
                fill_color=BLUE_E,
                dot_color=WHITE,
            ).replace(number, dim_to_match=1)
            for n, number in enumerate(numbers)
        ))
        for die in die_faces:
            die.dots.set_stroke(WHITE, 1)
        die_faces.set_stroke(width=1)

        return die_faces

    def get_mean_and_standard_deviation(self, distribution):
        prob_value_pairs = list(zip(distribution, it.count(1)))
        mu = sum(p * x for p, x in prob_value_pairs)
        sigma = math.sqrt(sum(p * (x - mu)**2 for p, x in prob_value_pairs))
        return mu, sigma

    def get_mean_labels(self, plots, color=PINK, num_decimal_places=1):
        mu = self.get_mean_and_standard_deviation(self.distribution)[0]
        mean_labels = VGroup()
        for n, plot in zip(it.count(1), plots):
            axes = plot[0]
            label = Tex(fR"{n}\mu = {np.round(n * mu, num_decimal_places)}")
            if n == 1:
                label[0].scale(0, about_edge=RIGHT)
            v_line = Line(*axes.y_axis.get_start_and_end())
            v_line.move_to(axes.c2p(n * mu - 0.5, 0), DOWN)
            label.shift(
                v_line.get_top() + MED_SMALL_BUFF * UP - label[:2].get_bottom()
            )
            mean_labels.add(VGroup(v_line, label))

        mean_labels.set_color(color)
        return mean_labels

    def get_sd_labels(self, plots, color=RED):
        mu, sigma = self.get_mean_and_standard_deviation(self.distribution)

        sd_labels = VGroup()
        for n, plot in zip(it.count(1), plots):
            axes = plot[0]
            v_lines = Line(*axes.y_axis.get_start_and_end()).replicate(2)
            v_lines[0].move_to(axes.c2p(n * mu - math.sqrt(n) * sigma - 0.5, 0), DOWN)
            v_lines[1].move_to(axes.c2p(n * mu + math.sqrt(n) * sigma - 0.5, 0), DOWN)

            arrows = VGroup(
                FillArrow(v_lines.get_center(), v_lines[0].get_center()),
                FillArrow(v_lines.get_center(), v_lines[1].get_center()),
            )
            for arrow in arrows:
                arrow.scale(0.75)
            arrows.move_to(v_lines)

            if n == 1:
                sigma_label = Tex(fR"\sigma")
            else:
                sigma_label = Tex(fR"\sqrt{n} \cdot \sigma")
            sigma_label.scale(0.8)
            sigma_label.next_to(arrows[1], UP, SMALL_BUFF)

            sd_labels.add(VGroup(
                v_lines,
                arrows,
                sigma_label,
            ))
        sd_labels.set_color(color)

        return sd_labels

    def realign_distributions(self, all_bars, labels, mean_lines, sd_lines):
        frame = self.frame

        bar_groups = VGroup()
        for bars, mean_line, sd_line in zip(all_bars, mean_lines, sd_lines):
            bar_group = VGroup(bars, mean_line, sd_line)
            bar_group.target = bar_group.generate_target()
            bar_group.target.shift(
                (frame.get_center()[0] - mean_line.get_x()) * RIGHT
            )
            bar_groups.add(bar_group)

        labels.target = labels.generate_target()
        for label, bars in zip(labels.target, all_bars):
            label.match_y(bars)
            label.set_x(0)
        labels.target.set_x(frame.get_right()[0] - 1, RIGHT)

        self.play(
            MoveToTarget(labels),
            LaggedStartMap(MoveToTarget, bar_groups, lag_ratio=0.01),
            run_time=2
        )

    def rescale_distributions(self, all_bars, mean_lines, sd_lines):
        arrows = VGroup(*(
            self.get_rescaling_arrows(bars, n)
            for n, bars in zip(it.count(2), all_bars[1:])
        ))

        self.play(Write(arrows, lag_ratio=0.01))

        def get_factor(n):
            return math.sqrt(n)

        self.play(
            LaggedStart(*(
                bars.animate.stretch(
                    1 / get_factor(n), 0,
                    about_point=lines.get_center()
                ).stretch(get_factor(n), 1, about_edge=DOWN)
                for n, bars, lines in zip(it.count(2), all_bars[1:], sd_lines)
            )),
            LaggedStart(*(
                lines.animate.stretch(
                    1 / get_factor(n), 0,
                )
                for n, lines in zip(it.count(2), sd_lines[1:])
            )),
            Animation(mean_lines),
            LaggedStart(*(
                arrow.animate.shift(arrow.get_vector())
                for arrow_pair in arrows
                for arrow in arrow_pair
            )),
            run_time=3
        )
        self.wait()
        self.play(FadeOut(arrows))

    def get_center_of_mass_base(self, bars):
        dist = np.array([bar.get_height() for bar in bars])
        dist /= dist.sum()
        mu = sum(p * x for p, x in zip(dist, it.count()))
        return bars.get_corner(DL) + mu * bars[0].get_width() * RIGHT

    def get_rescaling_arrows(self, bars, n):
        dist = np.array([bar.get_height() for bar in bars])
        dist /= dist.sum()

        mu = sum(p * x for p, x in zip(dist, it.count()))
        sigma = math.sqrt(sum(p * (x - mu)**2 for p, x in zip(dist, it.count())))
        bar_width = bars[0].get_width()
        length = sigma * bar_width
        center = bars.get_corner(DL) + mu * bar_width * RIGHT
        center += bars.get_height() * UP / 2.0

        kw = dict(fill_color=RED)

        arrows = VGroup(*(
            FillArrow(ORIGIN, length * vect, **kw).move_to(
                center - 3.0 * sigma * bar_width * vect,
                -vect
            )
            for vect in [LEFT, RIGHT]
        ))
        labels = Tex(Rf"\sigma \sqrt{{{n}}}").replicate(2)
        for arrow, label in zip(arrows, labels):
            label.next_to(arrow, UP, buff=0)
            label.set_max_width(arrow.get_width())
            label[R"\sigma"].set_color(RED)
            arrow.add(label)
        return arrows

    def show_sample_sum(self, plot, distribution, n, low_plot=None):
        axes, bars = plot

        samples = np.random.choice(self.values, size=n, p=distribution)
        bar_highlights = VGroup(*(
            bars[sample - 1].copy()
            for sample in samples
        ))
        bar_highlights.set_fill(YELLOW, 1)

        if low_plot:
            low_bar_highlight = low_plot[1][sum(samples) - 1].copy()
            low_bar_highlight.set_fill(YELLOW, 1)
        else:
            low_bar_highlight = VMobject()

        tips = get_sample_markers(bars, samples)

        sum_expr = VGroup()
        for sample in samples:
            sum_expr.add(Integer(sample))
            sum_expr.add(Tex("+"))
        sum_expr.remove(sum_expr[-1])
        sum_expr.add(Tex("="))
        sum_expr.add(Integer(sum(samples), color=YELLOW))
        sum_expr.arrange(RIGHT, buff=0.15)

        sum_expr.scale(1.25)
        sum_expr.next_to(plot, RIGHT, buff=2.5)

        kw = dict(int_func=np.ceil)
        self.play(
            ShowIncreasingSubsets(tips, **kw),
            ShowSubmobjectsOneByOne(bar_highlights, remover=True, **kw),
            ShowIncreasingSubsets(sum_expr[0:-1:2], **kw),
            ShowIncreasingSubsets(sum_expr[1::2], **kw),
            run_time=0.5
        )
        self.wait(0.1)
        self.add(sum_expr)
        self.add(low_bar_highlight)
        self.wait()
        self.play(LaggedStartMap(FadeOut, VGroup(tips, sum_expr, low_bar_highlight)), run_time=0.5)


class ExpDistSumDistributions(DiceSumDistributions):
    n_examples = 7
    distribution = EXP_DISTRIBUTION

    def construct(self):
        # Setup all plots
        distributions = [
            [1 / 6] * 6,
            list(self.distribution),
        ]

        plots_list = VGroup()
        for dist in distributions:
            self.distribution = dist
            plots = VGroup(*(
                self.get_sum_distribution_plot(
                    n,
                    y_max=(0.2 if n > 1 else 0.4)
                )
                for n in range(1, self.n_examples + 1)
            ))
            plots.scale(0.9)
            plots.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
            plots.to_corner(UL)

            plots_list.add(plots)

        plots = plots_list[0]
        labels, die_labels = [
            VGroup(*(
                self.get_plot_label(plot, n, die_face)
                for plot, n in zip(plots, it.count(1))
            ))
            for die_face in [False, True]
        ]

        self.add(plots)
        self.add(die_labels)

        # Show new distribution
        self.play(
            Transform(plots, plots_list[1], run_time=3, lag_ratio=0.001),
            die_labels[0].animate.shift(0.25 * RIGHT),
        )
        self.wait()

        # Show pairs of samples
        self.play(
            FadeOut(plots[2:]),
            FadeOut(die_labels[2:]),
        )

        for _ in range(10):
            self.show_sample_sum(plots[0], distributions[1], 2, plots[1])

        self.play(ShowCreationThenFadeAround(VGroup(plots[1], die_labels[1])))
        self.wait()

        # Show triplet of samples
        plots[1].save_state()
        die_labels[1].save_state()
        self.play(
            FadeIn(plots[2], DOWN),
            FadeIn(die_labels[2], DOWN),
            plots[1].animate.set_opacity(0.2),
            die_labels[1].animate.set_opacity(0.2),
        )

        for _ in range(10):
            self.show_sample_sum(plots[0], distributions[1], 3, plots[2])
        self.play(Restore(plots[1]), Restore(die_labels[1]))

        # Replace labels
        labels[0].move_to(die_labels[0], LEFT)
        self.play(
            LaggedStartMap(FadeOut, die_labels, shift=UP, lag_ratio=0.25),
            LaggedStartMap(FadeIn, labels, shift=UP, lag_ratio=0.25),
        )
        self.wait()

        # Show more plots
        frame = self.frame
        self.add(plots)
        self.play(
            frame.animate.set_height(plots.get_height() + 2).move_to(plots, LEFT).shift(LEFT),
            run_time=4
        )
        self.wait()

        # Show means and standard deviation lines
        mu, sigma = self.get_mean_and_standard_deviation(self.distribution)
        mean_labels = self.get_mean_labels(plots, num_decimal_places=2)
        mean_lines = VGroup(*(ml[0] for ml in mean_labels))
        mu_labels = VGroup(*(ml[1] for ml in mean_labels))

        sd_labels = self.get_sd_labels(plots)
        sd_lines = VGroup(*(sdl[0] for sdl in sd_labels))
        sd_arrows = VGroup(*(sdl[1] for sdl in sd_labels))
        sigma_labels = VGroup(*(sdl[2] for sdl in sd_labels))

        all_axes = VGroup(*(plot[0] for plot in plots))
        arrows = VGroup(*(
            FillArrow(axes.c2p(0, 0), axes.c2p(n * mu, 0)).move_to(
                axes.y_axis.pfp(0.75), LEFT
            ).scale(0.7)
            for n, axes in zip(it.count(1), all_axes[1:])
        ))
        arrows.set_color(PINK)

        self.play(
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.2),
            LaggedStartMap(FadeIn, mean_lines, shift=RIGHT, lag_ratio=0.2),
        )
        self.wait()

        for line in sd_lines:
            line.save_state()
            line.stretch(0, 0)
            line.set_opacity(0)

        self.play(
            FadeOut(arrows),
            LaggedStartMap(Restore, sd_lines),
            LaggedStartMap(FadeIn, sd_arrows)
        )
        self.wait()

        # Quantify means
        frame.target = frame.generate_target()
        frame.target.set_height(5)
        frame.target.move_to(plots[0], DOWN)
        frame.target.shift(DOWN)
        frame_around_plot0 = frame.target.copy()

        self.play(
            MoveToTarget(frame),
            FadeOut(sd_lines, lag_ratio=0.1),
            FadeOut(sd_arrows, lag_ratio=0.1),
            run_time=5
        )
        self.play(Write(mu_labels[0]))
        self.wait()

        for n in range(6):
            frame.target = frame.generate_target()
            frame.target.set_height(plots[:n + 2].get_height() + 2)
            frame.target.move_to(plots[n + 1], DL).shift(0.75 * DL)

            self.play(LaggedStart(
                MoveToTarget(frame),
                TransformFromCopy(*mu_labels[n:n + 2]),
                lag_ratio=0.5
            ))
            self.wait()

        # Quantify standard deviation
        # sigma = 1.38, if you're curious
        VGroup(sd_arrows, sigma_labels).shift(0.25 * UP)
        for label, arrows in zip(sigma_labels, sd_arrows):
            label.set_max_width(arrows[1].get_width())

        self.play(
            LaggedStartMap(FadeIn, sd_lines, scale=2),
            LaggedStartMap(FadeIn, sd_arrows, scale=2),
            FadeOut(mu_labels, lag_ratio=0.01),
        )
        self.play(
            frame.animate.become(frame_around_plot0).set_anim_args(run_time=5),
            Write(sigma_labels[0]),
        )
        self.wait()

        for n in range(6):
            frame.target = frame.generate_target()
            frame.target.set_height(plots[:n + 2].get_height() + 2)
            frame.target.move_to(plots[n + 1], DL).shift(0.75 * DL)

            self.play(LaggedStart(
                MoveToTarget(frame),
                TransformFromCopy(*sigma_labels[n:n + 2]),
                lag_ratio=0.5
            ))
            self.wait()

        self.play(
            FadeOut(sigma_labels, lag_ratio=0.1),
            FadeOut(sd_arrows, lag_ratio=0.1),
        )
        self.add(mean_lines, sd_lines)

        # Realign and rescale
        all_axes = VGroup(*(plot[0] for plot in plots))
        all_bars = VGroup(*(plot[1] for plot in plots))
        all_bars[1].stretch(0.8, 1, about_edge=DOWN)

        self.play(FadeOut(all_axes))
        self.realign_distributions(all_bars, labels, mean_lines, sd_lines)

        big_mean_line = Line(mean_lines.get_top(), mean_lines.get_bottom())
        big_mean_line.set_stroke(PINK, 5)
        big_mean_line.insert_n_curves(20)
        self.play(VShowPassingFlash(big_mean_line, run_time=2, time_width=2.0))

        self.wait()
        self.rescale_distributions(all_bars, mean_lines, sd_lines)

        big_sd_lines = Line(UP, DOWN).replicate(2)
        big_sd_lines.arrange(RIGHT)
        big_sd_lines.replace(sd_lines, stretch=True)
        big_sd_lines.set_stroke(RED, 5)
        big_sd_lines.insert_n_curves(20)
        self.play(*(
            VShowPassingFlash(line, run_time=2, time_width=2.0)
            for line in big_sd_lines
        ))

        self.wait()
        self.play(
            FadeOut(mean_lines),
            FadeOut(sd_lines),
            lag_ratio=0.1
        )

        # Show bell curves
        axes = Axes(
            (-5, 5), (0, 1, 0.25),
            width=0.45 * frame.get_width(),
            height=0.5 * frame.get_height(),
        )
        axes.next_to(frame.get_left(), RIGHT, buff=1)
        axes.x_axis.add_numbers(font_size=36)
        axes.y_axis.add_numbers(np.arange(0.25, 1.25, 0.25), font_size=36, num_decimal_places=2)
        graph = axes.get_graph(lambda x: np.exp(-0.5 * x**2) / math.sqrt(2 * PI))
        graph.set_stroke(YELLOW, 3)

        graph_label = Tex(R"{1 \over \sqrt{2\pi}} e^{-{1 \over 2}x^2}")
        graph_label.set_height(0.8 * graph.get_height())
        graph_label.move_to(graph.get_corner(UL), DL)

        box = SurroundingRectangle(graph_label)
        box.set_stroke(YELLOW, 1)
        words = Text("We'll unpack this\n in a moment")
        words.match_width(box)
        words.next_to(box, UP, buff=LARGE_BUFF)

        bar_shift = 5 * RIGHT

        self.play(LaggedStart(
            FadeIn(axes),
            all_bars.animate.shift(bar_shift),
            ShowCreation(graph),
            Write(graph_label),
            lag_ratio=0.25
        ))
        self.wait()
        self.play(
            Write(words),
            ShowCreation(box)
        )
        self.wait()
        self.play(FadeOut(words), FadeOut(box))

        mean_lines.shift(bar_shift)
        sd_lines.shift(bar_shift)

        # Map bell curve over plots
        target_curves = VGroup()
        for bars, mean_line in zip(all_bars, mean_lines):
            curve = graph.copy()
            curve.replace(bars, dim_to_match=1)
            curve.set_width(sd_lines[0].get_width() * 4, stretch=True)
            curve.match_x(mean_line)
            target_curves.add(curve)

        self.play(LaggedStart(*(
            TransformFromCopy(graph, curve)
            for curve in target_curves
        )))
        self.wait()


class UDistSumDistributions(ExpDistSumDistributions):
    distribution = U_SHAPED_DISTRIBUTION
