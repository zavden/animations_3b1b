# ==============================================================================
# Scene:      XInMovingAverageGraphs
# Source:     videos/_2022/borwein/supplements.py (lines 207-243)
# Category:   1 · Renders unmodified
# Includes code copied from: _2022/borwein/main.py
#
# Run from this folder:
#     manimgl XInMovingAverageGraphs.py XInMovingAverageGraphs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2022/borwein/main.py -----

def rect_func(x):
    result = np.zeros_like(x)
    result[(-0.5 < x) & (x < 0.5)] = 1.0
    return result


class MovingAverages(InteractiveScene):
    sample_resolution = 1000
    graph_color = BLUE
    window_color = GREEN
    window_opacity = 0.35
    n_iterations = 8
    rect_scalar = 1.0
    quick_transitions = False

    def construct(self):
        # Add rect graph
        axes = self.get_axes()
        rs = self.rect_scalar
        rect_graph = axes.get_graph(
            lambda x: rect_func(x / rs),
            discontinuities=[-0.5 * rs, 0.5 * rs]
        )
        rect_graph.set_stroke(self.graph_color, 3)
        rect_def = self.get_rect_func_def()
        rect_def.to_corner(UR)
        rect_graph.axes = axes

        drawing_dot = GlowDot()
        drawing_dot.path = rect_graph
        drawing_dot.add_updater(lambda m: m.move_to(m.path.pfp(1)))

        self.add(axes)
        self.add(rect_def)
        self.add(drawing_dot)
        self.play(ShowCreation(rect_graph), run_time=3, rate_func=linear)
        self.play(FadeOut(drawing_dot))
        self.wait()

        # Add f1 label
        f1_label = OldTex("f_1(x) = ")
        f1_label.next_to(rect_def, LEFT, buff=0.2)

        self.play(Write(f1_label, stroke_color=WHITE))
        self.wait()

        f1_label_group = VGroup(f1_label, rect_def)
        rect_graph.func_labels = f1_label_group

        # Make room for new graph
        low_axes = self.get_axes().to_edge(DOWN, buff=MED_SMALL_BUFF)

        self.play(
            f1_label_group.animate.set_height(0.7, about_edge=UR),
            VGroup(axes, rect_graph).animate.to_edge(UP),
            TransformFromCopy(axes, low_axes)
        )
        self.wait()

        # Create all convolutions
        sample_resolution = self.sample_resolution
        xs = np.linspace(-rs, rs, int(2 * rs * sample_resolution + 1))
        k_range = list(range(3, self.n_iterations * 2 + 1, 2))
        graphs = [rect_graph, *self.get_all_convolution_graphs(
            xs, rect_func(xs / rs), low_axes, k_range
        )]
        for graph in graphs:
            graph.match_style(rect_graph)

        # Show all convolutions
        prev_graph = rect_graph
        prev_graph_label = f1_label_group

        for n in range(1, self.n_iterations):
            anim_time = (0.01 if self.quick_transitions else 1.0)
            # Show moving average, first with a pass, then with time to play
            window_group = self.show_moving_average(axes, low_axes, graphs[n], k_range[n - 1])

            # Label low graph
            fn_label = OldTex(f"f_{{{n + 1}}}(x)", font_size=36)
            fn_label.move_to(low_axes.c2p(0.5 * rs, 1), UL)
            fn0_label = OldTex(f"f_{{{n + 1}}}(0) = " + ("1.0" if n < self.n_iterations - 1 else "0.9999999999852937..."), font_size=36)
            fn0_label.next_to(fn_label, DOWN, aligned_edge=LEFT)

            self.play(Write(fn_label, stroke_color=WHITE), run_time=anim_time)
            self.wait(anim_time)

            # Note plateau width, color plateau
            width = max(rs - sum((1 / k for k in range(3, 2 * n + 3, 2))), 0)
            plateau = Line(low_axes.c2p(-width / 2, 1), low_axes.c2p(width / 2, 1))
            if width < 0:
                plateau.set_width(0)
            plateau.set_stroke(YELLOW, 3)
            brace = Brace(plateau, UP)
            brace_label = brace.get_tex(self.get_brace_label_tex(n))
            brace_label.scale(0.75, about_edge=DOWN)

            self.play(
                GrowFromCenter(brace),
                GrowFromCenter(plateau),
                Write(brace_label, stroke_color=WHITE),
                run_time=anim_time,
            )
            graphs[n].add(plateau)
            self.wait(anim_time)
            self.play(FadeIn(fn0_label, 0.5 * DOWN), run_time=anim_time)
            self.wait()

            # Remove window
            self.play(LaggedStartMap(FadeOut, window_group), run_time=anim_time)

            # Put lower graph up top
            new_low_axes = self.get_axes()
            new_low_axes.move_to(low_axes)
            shift_value = axes.c2p(0, 0) - low_axes.c2p(0, 0)

            if n < self.n_iterations - 1:
                anims = [
                    FadeOut(mob, shift_value)
                    for mob in [axes, prev_graph, prev_graph_label]
                ]
                anims.append(FadeIn(new_low_axes, shift_value))
            else:
                shift_value = ORIGIN
                anims = []

            anims.extend([
                *(
                    mob.animate.shift(shift_value)
                    for mob in [low_axes, graphs[n], fn_label, fn0_label]
                ),
                FadeOut(VGroup(brace, brace_label), shift_value),
            ])

            self.play(*anims)

            prev_graph = graphs[n]
            prev_graph_label = VGroup(fn_label, fn0_label)
            axes = low_axes
            low_axes = new_low_axes

            graphs[n].axes = axes
            graphs[n].func_labels = prev_graph_label

        # Show all graphs together
        graphs[0].add(Line(
            graphs[0].axes.c2p(-0.5, 1),
            graphs[0].axes.c2p(0.5, 1),
            stroke_color=YELLOW,
            stroke_width=3.0,
        ))
        graph_groups = VGroup(*(
            VGroup(graph.axes, graph, graph.func_labels[1])
            for graph in graphs[:8]
        ))
        graph_groups.save_state()
        graph_groups.generate_target()
        graph_groups[:-2].set_opacity(0)
        graph_groups.target.arrange_in_grid(
            4, 2, v_buff=2.0, h_buff=1.0,
            aligned_edge=LEFT,
            fill_rows_first=False
        )
        for group in graph_groups.target:
            group[2].scale(2, about_edge=DL)

        graph_groups.target.set_height(FRAME_HEIGHT - 1)
        graph_groups.target.center().to_edge(LEFT)

        self.play(
            MoveToTarget(graph_groups),
            FadeOut(graphs[7].func_labels[0]),
            FadeOut(graphs[6].func_labels[0]),
        )
        self.wait()

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

    def show_moving_average(self, top_axes, low_axes, low_graph, k):
        rs = self.rect_scalar
        window = Rectangle(
            width=top_axes.x_axis.unit_size / k,
            height=top_axes.y_axis.unit_size * 1.5,
        )
        window.set_stroke(width=0)
        window.set_fill(self.window_color, self.window_opacity)
        window.move_to(top_axes.c2p(-rs, 0), DOWN)
        arrow_buff = min(SMALL_BUFF, window.get_width() / 2)
        arrow = Arrow(window.get_left(), window.get_right(), stroke_width=4, buff=arrow_buff)
        arrows = VGroup(arrow, arrow.copy().flip())
        arrows[0].shift(0.5 * arrow_buff * RIGHT)
        arrows[1].shift(0.5 * arrow_buff * LEFT)
        arrows.next_to(window.get_bottom(), UP, buff=0.5)
        width_label = OldTex(f"1 / {k}", font_size=24)
        width_label.set_backstroke(width=4)
        width_label.set_max_width(min(arrows.get_width(), 0.5))
        width_label.next_to(arrows, UP)
        window.add(arrows, width_label)
        window.add_updater(lambda w: w.align_to(top_axes.get_origin(), DOWN))

        v_line = DashedLine(
            window.get_top(),
            low_axes.c2p(low_axes.x_axis.p2n(window.get_bottom()), 0)
        )
        v_line.add_updater(lambda m, w=window: m.move_to(w.get_top(), UP))
        v_line.set_stroke(WHITE, 1)

        self.add(window)
        self.add(v_line)

        drawing_dot = GlowDot(color=window.get_color())
        drawing_dot.add_updater(lambda m, w=window, g=low_graph.copy(): m.move_to(
            g.quick_point_from_proportion(
                (low_axes.x_axis.p2n(w.get_center()) + rs) / (2 * rs)
            )
        ))
        drawing_dot.set_glow_factor(1)
        drawing_dot.set_radius(0.15)
        self.add(drawing_dot)
        self.play(
            ShowCreation(low_graph),
            window.animate.move_to(top_axes.c2p(rs, 0), DOWN),
            rate_func=bezier([0, 0, 1, 1]),
            run_time=(2.5 if self.quick_transitions else 5),
        )
        self.wait()
        return Group(window, v_line, drawing_dot)

    def get_brace_label_tex(self, n):
        result = "1"
        for k in range(3, 2 * n + 3, 2):
            result += "- " + f"1 / {k}"
        return result

    def get_rect_func_def(self):
        return Tex(
            R"""\text{rect}(x) :=
            \begin{cases}
                1 & \text{if } \text{-}\frac{1}{2} < x < \frac{1}{2} \\
                0 & \text{otherwise}
            \end{cases}"""
        )

    def get_axes(self, x_range=(-1, 1, 0.25), y_range=(0, 1, 0.25), width=13.0, height=2.5):
        axes = Axes(x_range=x_range, y_range=y_range, width=width, height=height)
        axes.add_coordinate_labels(
            x_values=np.arange(*x_range)[::2],
            y_values=np.arange(0, 1.0, 0.5),
            num_decimal_places=2, font_size=20
        )
        return axes



# ----- From _2022/borwein/supplements.py -----

class XInMovingAverageGraphs(MovingAverages):
    def construct(self):
        axes1, axes2 = self.get_axes(), self.get_axes()
        axes1.to_edge(UP)
        axes2.to_edge(DOWN).shift(0.15 * DOWN)

        # self.add(axes1, axes2)  # Remove

        # Labels
        x = -0.61
        y = 0.1
        xp1 = axes1.c2p(x, 0)
        x_label = OldTex(f"x = {x}", tex_to_color_map={"x": YELLOW})
        x_label.next_to(xp1, DOWN, buff=LARGE_BUFF)
        arrow = Arrow(x_label[0].get_top(), xp1, buff=0.2).set_color(YELLOW)

        h_line = DashedLine(axes2.c2p(0, y), axes2.c2p(x, y))
        h_line.set_stroke(RED, 2)

        us = axes1.x_axis.unit_size
        brace = Brace(Line(xp1 + us * LEFT / 6, xp1 + us * RIGHT / 6), DOWN)
        brace_text = brace.get_text("Average value\nin this window", font_size=36)

        self.play(
            Write(x_label),
            ShowCreation(arrow)
        )
        self.wait()
        self.play(ShowCreation(h_line))
        self.wait()
        self.play(
            FadeOut(x_label),
            FadeOut(arrow),
            GrowFromCenter(brace),
            FadeIn(brace_text, 0.5 * DOWN)
        )
        self.wait()
