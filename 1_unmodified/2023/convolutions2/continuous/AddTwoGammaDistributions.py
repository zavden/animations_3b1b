# ==============================================================================
# Scene:      AddTwoGammaDistributions
# Source:     videos/_2023/convolutions2/continuous.py (lines 741-856)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AddTwoGammaDistributions.py AddTwoGammaDistributions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import scipy.signal
import scipy.stats

def get_conv_graph(axes, f, g, dx=0.1):
    dx = 0.1
    x_min, x_max = axes.x_range[:2]
    x_samples = np.arange(x_min, x_max + dx, dx)
    f_samples = np.array([f(x) for x in x_samples])
    g_samples = np.array([g(x) for x in x_samples])
    full_conv = np.convolve(f_samples, g_samples)
    x0 = len(x_samples) // 2 - 1  # TODO, be smarter about this
    conv_samples = full_conv[x0:x0 + len(x_samples)]
    conv_graph = VMobject()
    conv_graph.set_stroke(TEAL, 2)
    conv_graph.set_points_smoothly(axes.c2p(x_samples, conv_samples * dx))
    return conv_graph


class RepeatedSamplesFromContinuousDistributions(InteractiveScene):
    sigma1 = 1.0
    sigma2 = 1.0

    graph_colors = [BLUE, RED, TEAL]
    graph_stroke_width = 2

    dot_fade_factor = 0.25

    def setup(self):
        super().setup()
        self.random_variables = self.get_random_variables()
        self.all_dots = Group()
        self.add(self.all_dots)

    def get_plots(self):
        # Axes and graphs
        all_axes = self.get_axes()
        left_axes = all_axes[:2]
        left_axes.arrange(DOWN, buff=1.5)
        left_axes.to_edge(LEFT)
        all_axes[2].center().to_edge(RIGHT)

        for axes in all_axes:
            axes.x_axis.add_numbers(font_size=16)
            axes.y_axis.set_stroke(opacity=0.5)

        pdfs = self.get_pdfs()
        graphs = VGroup(*(
            axes.get_graph(func).set_stroke(color)
            for axes, func, color in zip(
                all_axes,
                self.get_pdfs(),
                self.graph_colors
            )
        ))
        graphs.add(self.get_sum_graph(all_axes[2]))
        graphs.set_stroke(width=self.graph_stroke_width)

        # Labels
        labels = self.get_axes_labels(all_axes)

        plots = VGroup(*(
            VGroup(*tup)
            for tup in zip(all_axes, graphs, labels)
        ))
        return plots

    def get_axes(self):
        return VGroup(*(
            Axes(
                (-5, 5), (0, 0.5, 0.25),
                width=5.5,
                height=2,
            )
            for x in range(3)
        ))

    def get_axes_labels(self, all_axes):
        a1, a2, a3 = all_axes
        return VGroup(
            Tex("X").move_to(midpoint(a1.get_corner(UR), a1.get_top())),
            Tex("Y").move_to(midpoint(a2.get_corner(UR), a2.get_top())),
            Tex("X + Y").next_to(a3, UP, buff=1.0)
        )

    def repeated_samples(self, plots, n_repetitions, **kwargs):
        for n in range(n_repetitions):
            self.animate_samples(plots, **kwargs)

    def animate_samples(
        self,
        plots,
        time_between_samples=0.25,
        time_before_fade=1.0,
        animate=True,
    ):
        # Setup
        xy_samples = np.round(self.get_samples(), 2)
        sample_sum = sum(xy_samples)
        samples = [*xy_samples[:2], sample_sum]
        dots = Group()
        labels = VGroup()
        lines = VGroup()
        for sample, plot in zip(samples, plots):
            axes, graph, sym_label = plot
            dot = GlowDot(axes.c2p(sample, 0))
            label = DecimalNumber(sample)
            label.next_to(sym_label, DOWN)
            label.scale(0.75, about_edge=DOWN)
            label.set_fill(GREY_A)

            line = axes.get_v_line_to_graph(sample, graph, line_func=Line)
            line.set_stroke(YELLOW, 2)

            dots.add(dot)
            labels.add(label)
            lines.add(line)

        if len(plots) > 2:
            sum_label = VGroup(
                DecimalNumber(samples[0]),
                Tex("+") if samples[1] > 0 else Tex("-"),
                DecimalNumber(abs(samples[1])),
                Tex("="),
                DecimalNumber(samples[2]),
            )
            sum_label.arrange(RIGHT, buff=0.15)
            sum_label[-1].align_to(sum_label[0], DOWN)
            sum_label.match_height(labels[2])
            sum_label.match_style(labels[2])
            sum_label.move_to(labels[2], DL)
            labels.remove(labels[2])
            labels.add(sum_label)
            sum_label.shift((plots[2][2]["+"].get_x() - sum_label[1].get_x()) * RIGHT)

        # Animate
        for i in range(min(2, len(plots))):
            self.add(dots[i], labels[i], lines[i])
            if len(plots) > 2:
                self.add(sum_label[:2 * i + 1])
            self.wait(time_between_samples)
        if len(plots) > 2:
            self.play(LaggedStart(
                Transform(dots[0].copy(), dots[2].copy().set_opacity(0.5), remover=True),
                Transform(dots[1].copy(), dots[2].copy().set_opacity(0.5), remover=True),
                FadeTransform(sum_label[:3].copy(), sum_label[3:]),
                run_time=1.0 if animate else 0,
            ))
            self.add(sum_label)
            self.add(dots[2])
        self.wait(time_before_fade)
        kw = dict(run_time=0.25 if animate else 0)
        self.play(
            LaggedStart(*(
                dot.animate.set_radius(0.1).set_opacity(self.dot_fade_factor)
                for dot in dots
            ), **kw),
            LaggedStartMap(FadeOut, labels, **kw),
            LaggedStartMap(FadeOut, lines[:2], **kw),
        )
        self.all_dots.add(*dots)
        self.add(self.all_dots)

    def get_random_variables(self):
        return [
            scipy.stats.norm(0, self.sigma1),
            scipy.stats.norm(0, self.sigma2),
        ]

    def get_samples(self):
        return [
            np.round(var.rvs(), 2)
            for var in self.random_variables
        ]

    def get_pdfs(self):
        return [var.pdf for var in self.random_variables]

    def get_sum_graph(self, axes):
        graph = get_conv_graph(axes, *self.get_pdfs())
        graph.set_stroke(self.graph_colors[2])
        return graph


class AddTwoGammaDistributions(RepeatedSamplesFromContinuousDistributions):
    dot_fade_factor = 0.75

    def construct(self):
        # Plots
        plots = self.get_plots()
        self.add(plots)

        # Add graph labels
        kw = dict(font_size=30)
        graph_labels = VGroup(
            Tex("e^{-x}", **kw),
            Tex(R"\frac{1}{2} x^2 \cdot e^{-x}", **kw),
            Tex(R"\frac{1}{6} x^3 \cdot e^{-x}", **kw),
        )
        for plot, label, x in zip(plots, graph_labels, [1, 2, 3]):
            axes, graph, var_label = plot
            label.next_to(axes.i2gp(x, graph), UP, SMALL_BUFF)
            label.match_color(graph)
        graph_labels[0].shift(0.3 * UR)

        self.add(graph_labels)

        # Initial samples
        self.repeated_samples(
            plots, 40,
            animate=False,
            time_between_samples=0.1,
            time_before_fade=0.5
        )

        # Graph equation
        frame = self.frame
        fs_rect = FullScreenRectangle()
        fs_rect.set_stroke(GREY_B, 1)
        fs_rect.set_fill(BLACK, 1)
        fuller_rect = FullScreenRectangle()
        fuller_rect.set_fill(GREY_E, 1)
        fuller_rect.scale(3)
        self.add(fuller_rect, fs_rect, *self.mobjects)

        graph_groups = VGroup(*(
            VGroup(plot[1], label).copy()
            for plot, label in zip(plots, graph_labels)
        ))
        graph_groups.generate_target()
        for graph_group in graph_groups.target:
            graph_group[0].stretch(0.5, 0, about_edge=LEFT)
            graph_group[0].set_stroke(width=4)
            graph_group[1].shift(SMALL_BUFF * UP)

        kw = dict(font_size=96)
        lp, rp = parens = Tex("()", **kw)
        parens.stretch(1.5, 1)
        parens.match_height(graph_groups.target[0])
        equation = VGroup(
            lp.copy(), graph_groups.target[0], rp.copy(),
            Tex("*", **kw),
            lp.copy(), graph_groups.target[1], rp.copy(),
            Tex("=", **kw),
            graph_groups.target[2],
        )
        equation.arrange(RIGHT, buff=0.5)
        equation[:3].space_out_submobjects(0.9)
        equation[4:7].space_out_submobjects(0.9)
        equation.next_to(plots, UP, buff=1.5)
        symbols = VGroup(*(
            mob for mob in equation
            if mob not in graph_groups.target
        ))

        self.play(
            frame.animate.set_height(13, about_point = 3 * DOWN),
            FadeIn(fuller_rect),
            FadeIn(fs_rect),
            MoveToTarget(graph_groups, run_time=2),
            Write(symbols, run_time=2),
        )
        self.wait()

        # Label convolution
        conv_label = Text("Convolution", font_size=72)
        arrow = Vector(DOWN)
        arrow.next_to(equation[3], UP)
        conv_label.next_to(arrow, UP)
        VGroup(conv_label, arrow).set_color(YELLOW)
        self.play(Write(conv_label), GrowArrow(arrow))

        # More repeated samples
        self.repeated_samples(
            plots, 50,
            animate=False,
            time_between_samples=0.1,
            time_before_fade=0.5
        )

    def get_axes(self):
        kw = dict(width=5.5, height=2,)
        return VGroup(
            Axes((0, 10), (0, 1.0, 0.25), **kw),
            Axes((0, 10), (0, 0.5, 0.25), **kw),
            Axes((0, 10), (0, 0.5, 0.25), **kw),
        )

    def get_random_variables(self):
        return [
            scipy.stats.gamma(1),
            scipy.stats.gamma(3),
        ]

    def get_sum_graph(self, axes):
        var = scipy.stats.gamma(4)
        return axes.get_graph(
            var.pdf,
            color=self.graph_colors[2]
        )
