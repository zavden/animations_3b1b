# ==============================================================================
# Scene:      RepeatedConvolution
# Source:     videos/_2023/convolutions2/continuous.py (lines 1824-2063)
# Category:   1 · Renders unmodified
# Includes code copied from: _2022/borwein/main.py, _2022/convolutions/discrete.py
#
# Run from this folder:
#     manimgl RepeatedConvolution.py RepeatedConvolution -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import scipy.signal
import scipy.stats


# ----- From _2022/borwein/main.py -----

def rect_func(x):
    result = np.zeros_like(x)
    result[(-0.5 < x) & (x < 0.5)] = 1.0
    return result



# ----- From _2022/convolutions/discrete.py -----

def kinked_function(x):
    if x < -2:
        return 0
    elif x < -1:
        return -x - 2
    elif x < 1:
        return x
    elif x < 2:
        return -x + 2
    else:
        return 0



# ----- From _2023/convolutions2/continuous.py -----

def uniform(x):
    return 1.0 * (-0.5 < x) * (x < 0.5)


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


class MovingAverageAsConvolution(Convolutions):
    g_graph_x_step = 0.1
    jagged_product = True
    g_is_rect = True

    def construct(self):
        # Setup
        super().construct()
        s_indicator = self.s_indicator
        f_axes, g_axes, fg_axes, conv_axes = self.all_axes
        self.g_label.shift(0.25 * UP)
        self.fg_label.shift(0.25 * UP)

        y_axes = VGroup(*(axes.y_axis for axes in self.all_axes[1:3]))
        fake_ys = y_axes.copy()
        for fake_y in fake_ys:
            fake_y.stretch(1.2, 1)
        self.add(*fake_ys, *self.mobjects)

        conv_axes.y_axis.match_height(f_axes.y_axis)
        VGroup(conv_axes).match_y(f_axes)
        self.conv_graph.match_points(get_conv_graph(conv_axes, self.f, self.g))
        self.conv_label.next_to(conv_axes, DOWN, MED_LARGE_BUFF)

        # Sample values
        def set_t(t):
            return s_indicator.animate.set_x(g_axes.c2p(t, 0)[0])

        self.play(set_t(-2.5), run_time=2)
        self.play(set_t(2.5), run_time=8)
        self.wait()
        self.play(set_t(-1), run_time=3)
        self.wait()

        # Isolate to slice
        top_line, side_line = Line().replicate(2)
        top_line.add_updater(lambda l: l.put_start_and_end_on(*self.g_graph.get_anchors()[4:6]))
        side_line.add_updater(lambda l: l.put_start_and_end_on(*self.g_graph.get_anchors()[2:4]))

        top_line.set_stroke(width=0)
        self.add(top_line)

        left_rect, right_rect = fade_rects = FullScreenFadeRectangle().replicate(2)
        left_rect.add_updater(lambda m: m.set_x(top_line.get_left()[0], RIGHT))
        right_rect.add_updater(lambda m: m.set_x(top_line.get_right()[0], LEFT))

        self.play(FadeIn(fade_rects))
        self.play(set_t(-2), run_time=3)
        self.play(set_t(-0.5), run_time=3)
        self.wait()
        self.play(FadeOut(fade_rects))

        # Show rect dimensions
        get_k1 = self.k1_tracker.get_value
        get_k2 = self.k2_tracker.get_value
        top_label = DecimalNumber(1, font_size=24)
        top_label.add_updater(lambda m: m.set_value(1.0 / get_k1()))
        top_label.add_updater(lambda m: m.next_to(top_line, UP, SMALL_BUFF))
        side_label = DecimalNumber(1, font_size=24)
        side_label.add_updater(lambda m: m.set_value(get_k2()))
        side_label.add_updater(lambda m: m.next_to(side_line, LEFT, SMALL_BUFF))

        def change_ks(k1, k2, run_time=3):
            new_conv_graph = get_conv_graph(
                self.all_axes[3], self.f, lambda x: self.g(k1 * x) * k2,
            )
            new_conv_graph.match_style(self.conv_graph)
            self.play(
                self.k1_tracker.animate.set_value(k1),
                self.k2_tracker.animate.set_value(k2),
                Transform(self.conv_graph, new_conv_graph),
                run_time=run_time
            )

        top_line.set_stroke(WHITE, 3)
        side_line.set_stroke(RED, 3)
        self.play(
            ShowCreation(side_line),
            VFadeIn(side_label)
        )
        self.wait()
        self.play(
            ShowCreation(top_line),
            VFadeIn(top_label),
        )
        self.wait()

        # Change dimensions
        change_ks(0.5, 1)
        self.wait()
        change_ks(0.5, 0.5)
        self.play(set_t(-1.5), run_time=2)
        self.play(set_t(-0.25), run_time=2)
        self.wait()
        change_ks(2, 0.5)
        self.wait()
        change_ks(2, 2)
        self.wait()
        change_ks(4, 4)
        change_ks(1, 1)
        self.play(*map(FadeOut, [top_label, top_line, side_label, side_line]))

        # Show area
        rect = Rectangle()
        rect.set_fill(YELLOW, 0.5)
        rect.set_stroke(width=0)
        rect.set_gloss(1)
        rect.add_updater(lambda m: m.set_width(g_axes.x_axis.unit_size / get_k1(), stretch=True))
        rect.add_updater(lambda m: m.set_height(g_axes.y_axis.unit_size * get_k2(), stretch=True))
        rect.add_updater(lambda m: m.set_x(s_indicator.get_x()))
        rect.add_updater(lambda m: m.set_y(g_axes.get_origin()[1], DOWN))

        area_label = Tex(R"\text{Area } = 1", font_size=36)
        area_label.next_to(rect, UP, MED_LARGE_BUFF)
        area_label.to_edge(LEFT)
        arrow = Arrow(area_label.get_bottom(), rect.get_center())

        avg_label = TexText(R"Average value of\\$f(x)$ in the window", font_size=24)
        avg_label.move_to(area_label, DL)
        shift_value = self.all_axes[2].get_origin() - g_axes.get_origin() + 0.5 * DOWN
        avg_label.shift(shift_value)
        arrow2 = arrow.copy().shift(shift_value)

        self.play(
            Write(area_label, stroke_color=WHITE),
            ShowCreation(arrow),
            FadeIn(rect)
        )
        self.wait()
        self.play(
            FadeIn(avg_label, lag_ratio=0.1),
            ShowCreation(arrow2)
        )
        self.wait()
        for k in [1.4, 0.8, 1.0, 4.0, 10.0, 1.0]:
            change_ks(k, k)
        self.play(*map(FadeOut, [area_label, arrow, avg_label, arrow2]))

        # More ambient variation
        self.play(set_t(-2.5), run_time=3)
        self.play(set_t(2.5), run_time=8)
        self.play(set_t(0), run_time=4)
        change_ks(20, 20)
        self.wait()
        change_ks(10, 10)
        self.wait()
        change_ks(0.2, 0.2, run_time=12)
        self.wait()

    def f(self, x):
        return kinked_function(x)

    def g(self, x):
        return rect_func(x)


class RepeatedConvolution(MovingAverageAsConvolution):
    resolution = 0.01
    n_iterations = 12
    when_to_renormalize = 5
    f_label_tex = "f_1(x)"
    g_label_tex = "f_1(s - x)"
    fg_label_tex = R"f_1(x) \cdot f_1(s - x)"
    conv_label_tex = R"f_2(s) = [f_1 * f_1](s)"
    conv_y_stretch_factor = 1.0
    convolution_creation_time = 5
    pre_rescale_factor = 1.5
    lower_graph_target_area = 1.0

    def construct(self):
        # Clean the board
        dx = self.resolution
        axes1, axes2, axes3, conv_axes = self.all_axes
        g_graph = self.g_graph

        x_min, x_max = axes1.x_range[:2]
        x_samples = np.arange(x_min, x_max + dx, dx)
        f_samples = np.array([self.f(x) for x in x_samples])
        g_samples = np.array([self.g(x) for x in x_samples])

        self.remove(
            self.f_graph,
            self.prod_graphs,
            self.conv_graph,
            self.conv_graph_dot,
            self.conv_graph_line,
        )
        for axes in self.all_axes[:3]:
            axes.x_label.set_opacity(0)

        # New f graph
        f_graph = g_graph.copy()
        f_graph.clear_updaters()
        f_graph.set_stroke(BLUE, 3)
        f_graph.shift(axes1.get_origin() - axes2.get_origin())

        self.add(f_graph)

        # New prod graph
        def update_prod_graph(prod_graph):
            s = self.get_s()
            prod_samples = np.array([
                f_sample * self.g(s - x)
                for f_sample, x in zip(f_samples, x_samples)
            ])
            prod_graph.set_points_as_corners(
                axes3.c2p(x_samples, prod_samples)
            )

        prod_graph = VMobject()
        prod_graph.set_stroke(GREEN, 2)
        prod_graph.set_fill(BLUE_E, 1)
        prod_graph.add_updater(update_prod_graph)

        self.fg_label.shift(0.35 * UP)
        self.g_label.shift(0.35 * UP)

        self.add(prod_graph)
        self.add(self.fg_label)

        # Move convolution axes
        conv_axes.match_y(axes1)
        self.remove(self.conv_label)
        conv_label = self.get_conv_label(2)
        self.conv_label = conv_label
        self.add(conv_label)

        # Show repeated convolutions
        for n in range(1, self.n_iterations + 1):
            conv_samples, conv_graph = self.create_convolution(
                x_samples, f_samples, g_samples, conv_axes,
            )
            if n == self.when_to_renormalize:
                self.add_rescale_arrow()
            if n >= self.when_to_renormalize:
                self.rescale_conv(conv_axes, conv_graph, n)
            self.swap_graphs(f_graph, conv_graph, axes1, conv_axes, n)
            self.swap_labels(n, conv_graph)
            f_samples[:] = conv_samples

    def create_convolution(self, x_samples, f_samples, g_samples, conv_axes):
        # Prepare
        self.set_s(x_samples[0], animate=False)

        conv_samples, conv_graph = self.get_conv(
            x_samples, f_samples, g_samples, conv_axes
        )
        endpoint_dot = GlowDot(color=WHITE)
        endpoint_dot.add_updater(lambda m: m.move_to(conv_graph.get_points()[-1]))

        # Sweep
        self.play(
            self.set_s(x_samples[-1]),
            ShowCreation(conv_graph),
            UpdateFromAlphaFunc(
                endpoint_dot, lambda m, a: m.move_to(conv_graph.get_end()).set_opacity(min(6 * a, 1)),
            ),
            run_time=self.convolution_creation_time,
            rate_func=bezier([0, 0, 1, 1])
        )
        self.play(FadeOut(endpoint_dot, run_time=0.5))

        return conv_samples, conv_graph

    def swap_graphs(self, f_graph, conv_graph, f_axes, conv_axes, n):
        shift_value = f_axes.get_origin() - conv_axes.get_origin()
        conv_axes_copy = conv_axes.deepcopy()

        f_label = self.f_label
        new_f_label = Tex(f"f_{{{n + 1}}}(x)", **self.label_config)
        new_f_label.replace(self.conv_label[:len(new_f_label)])
        new_f_label[-2].set_opacity(0)

        f_group = VGroup(f_axes, f_graph, f_label)
        new_f_graph = conv_graph.copy()
        self.add(conv_axes_copy, new_f_graph)
        anims = [
            Transform(conv_axes_copy, f_axes, remover=True),
            new_f_graph.animate.shift(shift_value).match_style(f_graph),
            FadeOut(f_group, shift_value),
            new_f_label.animate.replace(f_label, dim_to_match=1).set_opacity(1),
        ]
        self.play(LaggedStart(*anims))
        self.remove(new_f_label, new_f_graph)
        f_graph.become(new_f_graph)
        f_label.become(new_f_label)
        self.add(f_axes, f_graph, f_label)

    def swap_labels(self, n, conv_graph):
        # Test
        new_conv_label = self.get_conv_label(n + 2)
        new_conv_label.replace(self.conv_label)
        prod_rhs = self.fg_label[6:]
        new_prod_rhs = Tex(f"f_{{{n + 1}}}(s - x)")
        new_prod_rhs.replace(prod_rhs, dim_to_match=1)

        to_remove = VGroup(
            self.conv_label[f"f_{{{n + 1}}}"],
            self.conv_label[f"f_{{{n}}}"],
            prod_rhs,
        )
        to_add = VGroup(
            new_conv_label[f"f_{{{n + 2}}}"],
            new_conv_label[f"f_{{{n + 1}}}"],
            new_prod_rhs,
        )
        anims = [
            LaggedStartMap(FadeOut, to_remove, shift=0.5 * UP),
            LaggedStartMap(FadeIn, to_add, shift=0.5 * UP),
            FadeOut(conv_graph),
        ]
        if hasattr(self, "rescaled_graphs"):
            anims.append(self.rescaled_graphs.animate.set_stroke(width=0.5, opacity=0.5))
        self.play(*anims, run_time=1)

        self.remove(self.conv_label)
        self.remove(new_prod_rhs)
        self.conv_label = new_conv_label
        prod_rhs.become(new_prod_rhs)
        self.add(self.conv_label)
        self.add(prod_rhs)

    def add_rescale_arrow(self):
        arrow = Vector(1.5 * DOWN)
        label = TexText(R"Rescale so that\\std. dev. = 1", font_size=30)
        label.next_to(arrow)
        self.rescale_label = VGroup(label, arrow)
        self.rescale_label.next_to(self.conv_label, DOWN)

        self.play(
            GrowArrow(arrow),
            FadeIn(label)
        )
        self.add(self.rescale_label)

    def rescale_conv(self, conv_axes, conv_graph, n):
        anims = []
        if not hasattr(self, "rescaled_axes"):
            self.rescaled_axes = conv_axes.copy()
            self.rescaled_axes.next_to(self.rescale_label, DOWN)
            self.rescaled_graphs = VGroup()
            anims.append(TransformFromCopy(conv_axes, self.rescaled_axes))

        factor = self.pre_rescale_factor / math.sqrt(n + 1)
        stretched_graph = conv_graph.copy()
        stretched_graph.stretch(factor, 0)
        stretched_graph.stretch(1 / factor, 1, about_edge=DOWN)

        new_graph = VMobject()
        new_graph.start_new_path(conv_axes.x_axis.get_start())
        new_graph.add_line_to(stretched_graph.get_start())
        new_graph.append_vectorized_mobject(stretched_graph)
        new_graph.add_line_to(conv_axes.x_axis.get_end())
        new_graph.match_style(stretched_graph)
        new_graph.shift(self.rescaled_axes.x_axis.pfp(0.5) - conv_axes.c2p(0, 0))
        area = get_norm(new_graph.get_area_vector())
        new_graph.stretch(self.lower_graph_target_area / area, 1, about_edge=DOWN)

        anims.append(TransformFromCopy(conv_graph, new_graph))
        self.play(*anims)

        self.rescaled_graphs.add(new_graph)
        self.add(self.rescaled_graphs)

    def get_conv(self, x_samples, f_samples, g_samples, axes):
        """
        Returns array of samples and graph
        """
        conv_samples = self.resolution * scipy.signal.fftconvolve(
            f_samples, g_samples, mode='same'
        )
        conv_graph = VMobject()
        conv_graph.set_points_as_corners(axes.c2p(x_samples, conv_samples))
        conv_graph.set_stroke(TEAL, 3)
        return conv_samples, conv_graph

    def get_s(self):
        return self.all_axes[1].x_axis.p2n(self.s_indicator.get_center())

    def set_s(self, s, animate=True):
        if animate:
            mob = self.s_indicator.animate
        else:
            mob = self.s_indicator
        return mob.set_x(self.all_axes[1].c2p(s)[0])

    def get_conv_label(self, n):
        lhs = f"f_{{{n}}}(s)"
        last = f"f_{{{n - 1}}}"
        result = Tex(lhs, "=", R"\big[", last, "*", "f_1", R"\big]", "(s)")
        result.set_height(0.5)
        result.next_to(self.all_axes[3], DOWN, MED_LARGE_BUFF)
        return result

    def f(self, x):
        return uniform(x)
