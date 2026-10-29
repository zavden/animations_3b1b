# ==============================================================================
# Scene:      RectConvolutionsNewNotation
# Source:     videos/_2023/convolutions2/continuous.py (lines 2144-2262)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/borwein/main.py
#
# Run from this folder:
#     manimgl RectConvolutionsNewNotation.py RectConvolutionsNewNotation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_all_convolution_graphs and get_rect_func_def do not exist in the class or its bases in the original (AttributeError); they are copied from MovingAverages in _2022/borwein/main.py:866 and :940
#   - x_axis.unit_size / y_axis.unit_size -> get_unit_size(): NumberLine.unit_size stopped being an attribute (manimgl #2402)
#   - get_rect_k_graph: x_range[2] = 1 / k (assignment on a tuple, fails) -> x_range=(min, max, 1 / k) passed to get_graph
#   - self.clear() at the start of construct: Convolutions.setup() draws the base scene and the scene builds its own layout on top (in the original, Grant erased it by hand in interactive mode)
#   - conv_labels[...][0][a:b] and Tex(...)[0] -> without the [0]: Tex is flat at glyph level, so the [0] only took the first glyph (the rect_k labels came out as an 'r')
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2022/borwein/main.py -----

def rect_func(x):
    result = np.zeros_like(x)
    result[(-0.5 < x) & (x < 0.5)] = 1.0
    return result



# ----- From _2023/convolutions2/continuous.py -----

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


class MovingAverageOfRectFuncs(Convolutions):
    f_graph_x_step = 0.01
    g_graph_x_step = 0.01
    jagged_product = True

    def construct(self):
        super().construct()
        s_indicator = self.s_indicator
        g_axes = self.all_axes[1]
        self.all_axes[3].y_axis.match_height(g_axes.y_axis)
        self.conv_graph.set_height(0.5 * g_axes.y_axis.get_height(), about_edge=DOWN, stretch=True)

        for t in [3, -3, 0]:
            self.play(s_indicator.animate.set_x(g_axes.c2p(t, 0)[0]), run_time=5)
        self.wait()

    def f(self, x):
        return rect_func(x / 2)

    def g(self, x):
        return 1.5 * rect_func(1.5 * x)


class RectConvolutionsNewNotation(MovingAverageOfRectFuncs):
    def construct(self):
        # CHANGE: Convolutions.setup() already draws the axes and graphs of the base scene; this scene builds its
        # own layout, so it is cleared first (in the original, Grant erased that by hand in interactive mode)
        self.clear()

        # Setup axes
        x_min, x_max = -1.0, 1.0
        all_axes = axes1, axes2, axes3 = VGroup(*(
            Axes(
                (x_min, x_max, 0.5), (0, 5),
                width=3.75, height=4
            )
            for x in range(3)
        ))
        all_axes.arrange(RIGHT, buff=LARGE_BUFF, aligned_edge=DOWN)
        for axes in all_axes:
            axes.x_axis.add_numbers(font_size=12, num_decimal_places=1)
        axes2.y_axis.add_numbers(font_size=12, num_decimal_places=0, direction=DL, buff=0.05)
        all_axes.move_to(DOWN)

        self.add(all_axes)

        # Prepare convolution graphs
        dx = 0.01
        xs = np.arange(x_min, x_max + dx, dx)
        k_range = list(range(3, 9, 2))
        conv_graphs = self.get_all_convolution_graphs(xs, rect_func(xs), axes3, k_range)
        VGroup(*conv_graphs).set_stroke(TEAL, 3)

        rect_defs = VGroup(
            self.get_rect_func_def(),
            *(self.get_rect_k_def(k) for k in k_range)
        )
        rect_defs.scale(0.75)
        rect_defs.next_to(axes2, UP)
        rect_defs[0][9:].scale(0.7, about_edge=LEFT)
        rect_defs[0].next_to(axes1, UP).shift_onto_screen()

        conv_labels = VGroup(
            Tex(R"\big[\text{rect} * \text{rect}_3\big](x)"),
            Tex(R"\big[\text{rect} * \text{rect}_3 * \text{rect}_5\big](x)"),
            Tex(R"\big[\text{rect} * \text{rect}_3 * \text{rect}_5 * \text{rect}_7 \big](x)"),
        )
        conv_labels.scale(0.75)
        conv_labels.match_x(axes3).match_y(rect_defs)

        # Show rect_1 * rect_3
        rect_graphs = VGroup(*(
            self.get_rect_k_graph(axes2, k)
            for k in [1, *k_range]
        ))
        rect_graphs[0].set_color(BLUE)
        rect_graphs[0].match_x(axes1)

        # CHANGE: NumberLine.unit_size is no longer an attribute (manimgl #2402); it is now the method get_unit_size()
        rect = Rectangle(axes2.x_axis.get_unit_size() / 3, axes2.y_axis.get_unit_size() * 3)
        rect.set_stroke(width=0)
        rect.set_fill(YELLOW, 0.5)
        rect.move_to(axes2.get_origin(), DOWN)

        self.add(*rect_graphs[:2])
        self.add(*rect_defs[:2])
        self.add(conv_graphs[0])

        self.play(FadeIn(rect))
        self.wait()

        self.play(
            # CHANGE: Tex(...) is now flat at glyph level (Tex(...)[0] is only the first glyph); the extra [0] is removed
            Transform(rect_defs[0][:4].copy(), conv_labels[0][1:5], remover=True, path_arc=-PI / 3),
            Transform(rect_defs[1][:5].copy(), conv_labels[0][6:11], remover=True, path_arc=-PI / 3),
            FadeIn(conv_labels[0], lag_ratio=0.1, time_span=(1.5, 2.5)),
            FadeOut(rect),
            run_time=2
        )
        self.wait()

        # Show the rest
        for n in range(2):
            left_graph = rect_graphs[n] if n == 0 else conv_graphs[n - 1]
            lefs_label = rect_defs[n] if n == 0 else conv_labels[n - 1]
            k = 2 * n + 5
            # CHANGE: NumberLine.unit_size is no longer an attribute (manimgl #2402); it is now the method get_unit_size()
            new_rect = Rectangle(axes2.x_axis.get_unit_size() / k, axes2.y_axis.get_unit_size() * k)
            new_rect.set_stroke(width=0)
            new_rect.set_fill(YELLOW, 0.5)
            new_rect.move_to(axes2.get_origin(), DOWN)
            self.play(
                FadeOut(left_graph, 1.5 * LEFT),
                FadeOut(lefs_label, 1.5 * LEFT),
                FadeOut(rect_defs[n + 1]),
                FadeOut(rect_graphs[n + 1]),
                conv_labels[n].animate.match_x(axes1),
                conv_graphs[n].animate.match_x(axes1),
            )
            self.play(
                Write(rect_defs[n + 2], stroke_color=WHITE),
                ShowCreation(rect_graphs[n + 2]),
                FadeIn(new_rect),
                run_time=1,
            )
            self.wait()
            # CHANGE: Tex(...) is now flat at glyph level (Tex(...)[0] is only the first glyph); the extra [0] is removed
            left_conv = conv_labels[n][1:-4]
            r = len(left_conv) + 1
            self.play(
                Transform(left_conv.copy(), conv_labels[n + 1][1:r], remover=True, path_arc=-PI / 3),
                Transform(rect_defs[2][:5].copy(), conv_labels[n + 1][r + 1:r + 6], remover=True, path_arc=-PI / 3),
                FadeIn(conv_labels[n + 1], lag_ratio=0.1, time_span=(0.5, 1.5)),
                ShowCreation(conv_graphs[n + 1]),
            )
            self.play(FadeOut(new_rect))
            self.wait()

    # CHANGE: get_all_convolution_graphs and get_rect_func_def do not exist in this class (nor in its bases) in the
    # original; they are copied from MovingAverages in _2022/borwein/main.py (lines 866 and 940)
    def get_all_convolution_graphs(self, xs, ys, axes, k_range):
        result = []
        func_samples = [ys]
        for k in k_range:
            kernel = rect_func(k * xs)
            kernel /= sum(kernel)
            func_samples.append(np.convolve(
                func_samples[-1],  # Last function
                kernel,
                mode='same'
            ))
            new_graph = VMobject()
            new_graph.set_points_smoothly(axes.c2p(xs, func_samples[-1]))
            new_graph.origin = axes.c2p(0, 0)
            result.append(new_graph)
        result[0].make_jagged()
        return result

    def get_rect_func_def(self):
        return Tex(
            R"""\text{rect}(x) :=
            \begin{cases}
                1 & \text{if } \text{-}\frac{1}{2} < x < \frac{1}{2} \\
                0 & \text{otherwise}
            \end{cases}"""
        )

    def get_rect_k_graph(self, axes, k):
        # CHANGE: x_range is now a tuple (x_range[2] cannot be assigned); the sampling step is passed to get_graph
        x_range = (*axes.x_axis.x_range[:2], 1 / k)
        return axes.get_graph(
            lambda x: k * rect_func(k * x),
            x_range=x_range,
            discontinuities=(-1 / (2 * k), 1 / (2 * k)),
            stroke_color=YELLOW,
            stroke_width=3,
        )

    def get_rect_k_def(self, k):
        # CHANGE: Tex(...) is now flat at glyph level (Tex(...)[0] is only the first glyph); the [0] is removed
        return Tex(Rf"\text{{rect}}_{{{k}}}(x) := {k} \cdot \text{{rect}}({k}x)")
