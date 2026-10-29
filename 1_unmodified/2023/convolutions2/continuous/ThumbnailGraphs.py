# ==============================================================================
# Scene:      ThumbnailGraphs
# Source:     videos/_2023/convolutions2/continuous.py (lines 1601-1614)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThumbnailGraphs.py ThumbnailGraphs -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def wedge_func(x):
    return np.clip(-np.abs(x) + 1, 0, 1)


def double_lump(x):
    return 0.45 * np.exp(-6 * (x - 0.5)**2) + np.exp(-6 * (x + 0.5)**2)


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


class Convolutions(InteractiveScene):
    axes_config = dict(
        x_range=(-3, 3, 1),
        y_range=(-1, 1, 1.0),
        width=6,
        height=2,
    )
    f_graph_style = dict(stroke_color=BLUE, stroke_width=2)
    g_graph_style = dict(stroke_color=YELLOW, stroke_width=2)
    fg_graph_style = dict(stroke_color=GREEN, stroke_width=4)
    conv_graph_style = dict(stroke_color=TEAL, stroke_width=2)
    f_graph_x_step = 0.1
    g_graph_x_step = 0.1
    f_label_tex = "f(x)"
    g_label_tex = "g(s - x)"
    fg_label_tex = R"f(x) \cdot g(s - x)"
    conv_label_tex = R"[f * g](s) = \int_{-\infty}^\infty f(x) \cdot g(s - x) dx"
    label_config = dict(font_size=36)
    t_color = TEAL
    area_line_dx = 0.05
    jagged_product = True
    jagged_convolution = True
    g_is_rect = False
    conv_y_stretch_factor = 2.0

    def setup(self):
        super().setup()
        if self.g_is_rect:
            k1_tracker = self.k1_tracker = ValueTracker(1)
            k2_tracker = self.k2_tracker = ValueTracker(1)

        # Add axes
        all_axes = self.all_axes = self.get_all_axes()
        f_axes, g_axes, fg_axes, conv_axes = all_axes
        x_min, x_max = self.axes_config["x_range"][:2]

        self.disable_interaction(*all_axes)
        self.add(*all_axes)

        # Add f(x)
        f_graph = self.f_graph = f_axes.get_graph(self.f, x_range=(x_min, x_max, self.f_graph_x_step))
        f_graph.set_style(**self.f_graph_style)
        f_label = self.f_label = self.get_label(self.f_label_tex, f_axes)
        if self.jagged_product:
            f_graph.make_jagged()

        self.add(f_graph)
        self.add(f_label)

        # Add g(s - x)
        self.toggle_selection_mode()  # So triangle is highlighted
        s_indicator = self.s_indicator = ArrowTip().rotate(90 * DEGREES)
        s_indicator.set_height(0.15)
        s_indicator.set_fill(self.t_color, 0.8)
        s_indicator.move_to(g_axes.get_origin(), UP)
        s_indicator.add_updater(lambda m: m.align_to(g_axes.get_origin(), UP))

        def get_s():
            return g_axes.x_axis.p2n(s_indicator.get_center())

        self.get_s = get_s
        g_graph = self.g_graph = g_axes.get_graph(lambda x: 0, x_range=(x_min, x_max, self.g_graph_x_step))
        g_graph.set_style(**self.g_graph_style)
        if self.g_is_rect:
            x_min = g_axes.x_axis.x_min
            x_max = g_axes.x_axis.x_max
            g_graph.add_updater(lambda m: m.set_points_as_corners([
                g_axes.c2p(x, y)
                for s in [get_s()]
                for k1 in [k1_tracker.get_value()]
                for k2 in [k2_tracker.get_value()]
                for x, y in [
                    (x_min, 0), (-0.5 / k1 + s, 0), (-0.5 / k1 + s, k2), (0.5 / k1 + s, k2), (0.5 / k1 + s, 0), (x_max, 0)
                ]
            ]))
        else:
            g_axes.bind_graph_to_func(g_graph, lambda x: self.g(get_s() - x), jagged=self.jagged_product)

        g_label = self.g_label = self.get_label(self.g_label_tex, g_axes)

        s_label = self.s_label = VGroup(*Tex("s = "), DecimalNumber())
        s_label.arrange(RIGHT, buff=SMALL_BUFF)
        s_label.scale(0.5)
        s_label.set_backstroke(width=8)
        s_label.add_updater(lambda m: m.next_to(s_indicator, DOWN, buff=0.15))
        s_label.add_updater(lambda m: m[-1].set_value(get_s()))

        self.add(g_graph)
        self.add(g_label)
        self.add(s_indicator)
        self.add(s_label)

        # Show integral of f(x) * g(s - x)
        def prod_func(x):
            k1 = self.k1_tracker.get_value() if self.g_is_rect else 1
            k2 = self.k2_tracker.get_value() if self.g_is_rect else 1
            return self.f(x) * self.g((get_s() - x) * k1) * k2

        fg_graph = fg_axes.get_graph(lambda x: 0, x_range=(x_min, x_max, self.g_graph_x_step))
        pos_graph = fg_graph.copy()
        neg_graph = fg_graph.copy()
        for graph in f_graph, g_graph, fg_graph, pos_graph, neg_graph:
            self.disable_interaction(graph)
        fg_graph.set_style(**self.fg_graph_style)
        VGroup(pos_graph, neg_graph).set_stroke(width=0)
        pos_graph.set_fill(BLUE, 0.5)
        neg_graph.set_fill(RED, 0.5)

        get_discontinuities = None
        if self.g_is_rect:
            def get_discontinuities():
                k1 = self.k1_tracker.get_value()
                return [get_s() - 0.5 / k1, get_s() + 0.5 / k1]

        kw = dict(
            jagged=self.jagged_product,
            get_discontinuities=get_discontinuities,
        )
        fg_axes.bind_graph_to_func(fg_graph, prod_func, **kw)
        fg_axes.bind_graph_to_func(pos_graph, lambda x: np.clip(prod_func(x), 0, np.inf), **kw)
        fg_axes.bind_graph_to_func(neg_graph, lambda x: np.clip(prod_func(x), -np.inf, 0), **kw)

        self.prod_graphs = VGroup(fg_graph, pos_graph, neg_graph)

        fg_label = self.fg_label = self.get_label(self.fg_label_tex, fg_axes)

        self.add(pos_graph, neg_graph, fg_axes, fg_graph)
        self.add(fg_label)

        # Show convolution
        conv_graph = self.conv_graph = self.get_conv_graph(conv_axes)
        if self.jagged_convolution:
            conv_graph.make_jagged()
        conv_graph.set_style(**self.conv_graph_style)

        graph_dot = self.graph_dot = GlowDot(color=WHITE)
        graph_dot.add_updater(lambda d: d.move_to(conv_graph.quick_point_from_proportion(
            inverse_interpolate(x_min, x_max, get_s())
        )))
        graph_line = self.graph_line = Line(stroke_color=WHITE, stroke_width=1)
        graph_line.add_updater(lambda l: l.put_start_and_end_on(
            graph_dot.get_center(),
            [graph_dot.get_x(), conv_axes.get_y(), 0],
        ))
        self.conv_graph_dot = graph_dot
        self.conv_graph_line = graph_line

        conv_label = self.conv_label = Tex(self.conv_label_tex, **self.label_config)
        conv_label.match_x(conv_axes)
        conv_label.set_y(np.mean([conv_axes.get_y(UP), FRAME_HEIGHT / 2]))

        self.add(conv_graph)
        self.add(graph_dot)
        self.add(graph_line)
        self.add(conv_label)

    def get_all_axes(self):
        all_axes = VGroup(*(Axes(**self.axes_config) for x in range(4)))
        all_axes[:3].arrange(DOWN, buff=0.75)
        all_axes[3].next_to(all_axes[:3], RIGHT, buff=1.5)
        all_axes[3].y_axis.stretch(
            self.conv_y_stretch_factor, 1
        )
        all_axes.to_edge(LEFT)
        all_axes.to_edge(DOWN, buff=0.1)

        for i, axes in enumerate(all_axes):
            x_label = Tex("x" if i < 3 else "s", font_size=24)
            x_label.next_to(axes.x_axis.get_right(), UP, MED_SMALL_BUFF)
            axes.x_label = x_label
            axes.x_axis.add(x_label)
            axes.y_axis.ticks.set_opacity(0)
            axes.x_axis.ticks.stretch(0.5, 1)

        return all_axes

    def get_label(self, tex, axes):
        label = Tex(tex, **self.label_config)
        label.move_to(midpoint(axes.get_origin(), axes.get_right()))
        label.match_y(axes.get_top())
        return label

    def get_conv_graph(self, conv_axes):
        return get_conv_graph(conv_axes, self.f, self.g)

    def get_conv_s_indicator(self):
        g_s_indicator = VGroup(self.s_indicator, self.s_label)
        f_axes, g_axes, fg_axes, conv_axes = self.all_axes

        def get_s():
            return g_axes.x_axis.p2n(self.s_indicator.get_x())

        conv_s_indicator = g_s_indicator.copy()
        conv_s_indicator.add_updater(lambda m: m.become(g_s_indicator))
        conv_s_indicator.add_updater(lambda m: m.shift(
            conv_axes.c2p(get_s(), 0) - g_axes.c2p(get_s(), 0)
        ))
        return conv_s_indicator

    def f(self, x):
        return 0.5 * np.exp(-0.8 * x**2) * (0.5 * x**3 - 3 * x + 1)

    def g(self, x):
        return np.exp(-x**2) * np.sin(2 * x)


class ProbConvolutions(Convolutions):
    jagged_product = True

    def construct(self):
        # Hit most of previous setup
        f_axes, g_axes, fg_axes, conv_axes = self.all_axes
        f_graph, g_graph, prod_graphs, conv_graph = self.f_graph, self.g_graph, self.prod_graphs, self.conv_graph
        f_label, g_label, fg_label, conv_label = self.f_label, self.g_label, self.fg_label, self.conv_label
        s_indicator = self.s_indicator
        s_label = self.s_label
        self.remove(s_indicator, s_label)

        f_axes.x_axis.add_numbers(font_size=16, buff=0.1, excluding=[0])
        self.remove(f_axes, f_graph, f_label)

        y_label = Tex("y").replace(g_axes.x_label)
        g_label.shift(0.2 * UP)
        gy_label = Tex("g(y)", **self.label_config).replace(g_label, dim_to_match=1)
        gmx_label = Tex("g(-x)", **self.label_config).replace(g_label, dim_to_match=1)
        g_axes.x_label.set_opacity(0)
        self.remove(g_axes, g_graph, g_label)

        alt_fg_label = Tex(R"p_X(x) \cdot g(-x)", **self.label_config)
        alt_fg_label.move_to(fg_label)

        conv_label.shift_onto_screen()
        sum_label = Tex("[f * g](s)", **self.label_config)
        sum_label.move_to(conv_label)
        self.remove(fg_axes, prod_graphs, fg_label)
        conv_cover = SurroundingRectangle(conv_axes, buff=0.25)
        conv_cover.set_stroke(width=0)
        conv_cover.set_fill(BLACK, 0.5)
        self.add(conv_cover)

        # Show f
        f_term = conv_label["f(x)"][0]
        f_rect = SurroundingRectangle(f_term)
        f_rect.set_stroke(YELLOW, 2)

        self.play(ShowCreation(f_rect))
        self.play(
            TransformFromCopy(f_term, f_label),
            FadeIn(f_axes),
        )
        self.play(
            ShowCreation(f_graph),
            VShowPassingFlash(f_graph.copy().set_stroke(width=5)),
            run_time=2
        )
        self.wait()

        # Show g
        true_g_graph = g_axes.get_graph(self.g)
        true_g_graph.match_style(g_graph)

        g_term = conv_label["g"][1]
        g_rect = SurroundingRectangle(g_term, buff=0.05)
        g_rect.match_style(f_rect)

        self.play(ReplacementTransform(f_rect, g_rect))
        self.play(
            TransformFromCopy(g_term, gy_label),
            FadeIn(g_axes),
            FadeIn(y_label),
        )
        self.play(
            ShowCreation(true_g_graph),
            VShowPassingFlash(true_g_graph.copy().set_stroke(width=5)),
            run_time=2
        )
        self.wait()

        # Range over pairs of values
        int_rect = SurroundingRectangle(conv_label[re.compile(R"\\int.*")])
        x_rects = VGroup(*(
            SurroundingRectangle(x, buff=0.05)
            for x in conv_label["x"]
        ))
        VGroup(int_rect, *x_rects).match_style(g_rect)

        const_sum = 0.3
        x_tracker = ValueTracker(-1.0)
        y_tracker = ValueTracker()
        x_term = DecimalNumber(include_sign=True, edge_to_fix=RIGHT)
        y_term = DecimalNumber(include_sign=True)
        s_term = DecimalNumber(const_sum)
        equation = VGroup(x_term, y_term, Tex("="), s_term)
        VGroup(x_term, s_term).shift(0.05 * RIGHT)
        equation.arrange(RIGHT, buff=SMALL_BUFF)
        equation.match_x(conv_label)

        x_brace, y_brace, s_brace = braces = VGroup(*(
            Brace(term, UP, SMALL_BUFF)
            for term in [x_term, y_term, s_term]
        ))
        x_brace.add(x_brace.get_tex("x").set_color(BLUE))
        y_brace.add(y_brace.get_tex("y").set_color(YELLOW))
        s_brace.add(s_brace.get_tex("s").set_color(GREY_B))
        y_brace[-1].align_to(x_brace[-1], UP)
        alt_y_label = Tex("s - x")
        alt_y_label.space_out_submobjects(0.8)
        alt_y_label.move_to(y_brace[-1], UP)
        alt_y_label.set_color_by_tex_to_color_map({"s": GREY_B, "x": BLUE})

        def get_x():
            return x_tracker.get_value()

        def get_y():
            return const_sum - get_x()

        f_always(y_tracker.set_value, get_y)
        f_always(x_term.set_value, get_x)
        f_always(y_term.set_value, get_y)

        Axes.get_v_line_to_graph
        x_line = always_redraw(lambda: f_axes.get_v_line_to_graph(
            get_x(), f_graph, line_func=Line, color=WHITE
        ))
        y_line = always_redraw(lambda: g_axes.get_v_line_to_graph(
            get_y(), true_g_graph, line_func=Line, color=WHITE
        ))
        x_dot = GlowDot(color=BLUE)
        y_dot = GlowDot(color=YELLOW)
        f_always(x_dot.move_to, x_line.get_end)
        f_always(y_dot.move_to, y_line.get_end)

        self.play(ReplacementTransform(g_rect, int_rect))
        self.wait()
        self.play(LaggedStart(
            conv_cover.animate.set_opacity(1),
            FadeIn(equation),
            FadeIn(braces),
            VFadeIn(x_line),
            VFadeIn(y_line),
            FadeIn(x_dot),
            FadeIn(y_dot),
        ))
        for x in [1.0, -1.0]:
            self.play(x_tracker.animate.set_value(x), run_time=8)

        self.wait()
        self.remove(int_rect)
        self.play(*(
            ReplacementTransform(int_rect.copy(), x_rect)
            for x_rect in x_rects
        ))
        self.wait()
        self.play(FadeOut(x_rects, lag_ratio=0.5))
        self.play(
            FadeTransform(conv_label["s - x"].copy(), alt_y_label),
            y_brace[-1].animate.set_opacity(0)
        )
        self.remove(alt_y_label)
        y_brace[-1].become(alt_y_label)

        for x in [1.0, -1.0]:
            self.play(x_tracker.animate.set_value(x), run_time=8)

        self.play(LaggedStart(*map(FadeOut, [
            x_line, x_dot, y_line, y_dot,
            *equation, *braces
        ])), lag_ratio=0.2)

        # Flip g
        gsmx_rect = SurroundingRectangle(conv_label["g(s - x)"], buff=0.05)
        gsmx_rect.match_style(g_rect)

        g_axes_copy = g_axes.copy()
        g_axes_copy.add(y_label)
        true_group = VGroup(g_axes_copy, gy_label, true_g_graph)

        self.play(ShowCreation(gsmx_rect))
        self.wait()
        self.play(
            true_group.animate.to_edge(DOWN, buff=MED_SMALL_BUFF),
        )
        self.add(*true_group)
        g_axes.generate_target()
        g_axes.target.x_label.set_opacity(1),
        self.play(
            TransformMatchingShapes(gy_label.copy(), gmx_label),
            true_g_graph.copy().animate.flip().move_to(g_graph).set_anim_args(remover=True),
            MoveToTarget(g_axes),
        )
        self.add(g_graph)
        self.wait()
        self.play(FadeOut(true_group))

        # Show the parameter s
        self.play(
            s_indicator.animate.match_x(g_axes.c2p(2, 0)).set_anim_args(run_time=3),
            VFadeIn(s_indicator),
            VFadeIn(s_label),
            TransformMatchingTex(gmx_label, g_label, run_time=1),
        )
        self.wait()  # Play with the slider
        self.play(
            s_indicator.animate.match_x(g_axes.c2p(0.3, 0))
        )

        # Show product
        fg_rect = SurroundingRectangle(conv_label[R"f(x) \cdot g(s - x)"])
        fg_rect.match_style(g_rect)

        self.play(ReplacementTransform(gsmx_rect, fg_rect))
        self.play(LaggedStart(
            FadeTransform(f_axes.copy(), fg_axes),
            FadeTransform(g_axes.copy(), fg_axes),
            Transform(f_graph.copy(), prod_graphs[0].copy(), remover=True),
            Transform(g_graph.copy(), prod_graphs[0].copy(), remover=True),
            TransformFromCopy(
                VGroup(*f_label, *g_label),
                fg_label
            ),
            FadeOut(fg_rect),
            run_time=2,
        ))
        self.add(*prod_graphs)
        self.play(FadeIn(prod_graphs[1]))
        self.add(prod_graphs)
        # Play with the slider
        self.wait()
        self.play(
            s_indicator.animate.match_x(g_axes.c2p(-0.8, 0))
        )

        # Show convolution
        def get_s():
            return g_axes.x_axis.p2n(s_indicator.get_x())

        conv_s_indicator = self.get_conv_s_indicator()

        self.play(FadeOut(conv_cover))
        self.play(Transform(
            VGroup(indicator, s_label).copy().clear_updaters(),
            conv_s_indicator.copy().clear_updaters(),
            remover=True
        ))
        self.add(conv_s_indicator)
        # Play with the slider
        self.wait()
        self.play(s_indicator.animate.match_x(g_axes.c2p(-0.4, 0)))

    def highlight_several_regions(self, highlighted_xs=None, s=0, reference=None):
        # Highlight a few regions
        if highlighted_xs is None:
            highlighted_xs = np.arange(-1, 1.1, 0.1)

        g_axes = self.all_axes[1]
        highlight_rect = Rectangle(width=0.1, height=FRAME_HEIGHT / 2)
        highlight_rect.set_stroke(width=0)
        highlight_rect.set_fill(TEAL, 0.5)
        highlight_rect.move_to(g_axes.get_origin(), DOWN)
        highlight_rect.set_opacity(0.5)
        self.add(highlight_rect)

        last_label = VMobject()
        for x in highlighted_xs:
            x_tex = f"{{{np.round(x, 1)}}}"
            diff_tex = f"{{{np.round(s - x, 1)}}}"
            label = Tex(
                fR"p_X({x_tex}) \cdot p_Y({diff_tex})",
                tex_to_color_map={diff_tex: YELLOW, x_tex: BLUE},
                font_size=36
            )
            if reference:
                label.next_to(reference, UP, MED_LARGE_BUFF)
            else:
                label.next_to(ORIGIN, DOWN, LARGE_BUFF)

            highlight_rect.set_x(g_axes.c2p(x, 0)[0]),
            self.add(label)
            self.remove(last_label)
            self.wait(0.25)
            last_label = label
        self.play(FadeOut(last_label), FadeOut(highlight_rect))

    def f(self, x):
        return wedge_func(x)

    def g(self, x):
        return double_lump(x)


class ProbConvolutionControlled(ProbConvolutions):
    t_time_pairs = [(-2.5, 4), (2.5, 10), (-1, 6)]
    initial_t = 0

    def construct(self):
        s_indicator = self.s_indicator
        g_axes = self.all_axes[1]

        def set_t(t):
            return s_indicator.animate.set_x(g_axes.c2p(t, 0)[0])

        s_indicator.set_x(g_axes.c2p(self.initial_t, 0)[0])
        for t, time in self.t_time_pairs:
            self.play(set_t(t), run_time=time)


class ProbConvolutionControlledToMatchSlices(ProbConvolutionControlled):
    t_time_pairs = [(-1.5, 20), (1.5, 20), (-0.5, 20)]
    initial_t = 2


class AltSyncedConvolution(ProbConvolutionControlledToMatchSlices):
    t_time_pairs = [(1.0, 15), (-1.5, 10), (-3.0, 10), (1.0, 20)]
    initial_t = -3.0

    def f(self, x):
        return (x > -2) * np.exp(-2 - x)

    def g(self, x):
        return wedge_func(x)


class ThumbnailGraphs(AltSyncedConvolution):
    def construct(self):
        super().construct()
        s_indicator = self.s_indicator
        f_axes, g_axes = self.all_axes[:2]

        for axes in [f_axes, g_axes]:
            axes.set_stroke(width=4)
            axes.x_axis[1].set_stroke(width=0)
        for graph in [self.f_graph, self.g_graph, self.prod_graphs]:
            graph.set_stroke(width=8)

        s = -1.68
        s_indicator.set_x(g_axes.c2p(s, 0)[0])
