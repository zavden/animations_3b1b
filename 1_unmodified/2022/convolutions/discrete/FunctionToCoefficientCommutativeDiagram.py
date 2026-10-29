# ==============================================================================
# Scene:      FunctionToCoefficientCommutativeDiagram
# Source:     videos/_2022/convolutions/discrete.py (lines 1998-2130)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FunctionToCoefficientCommutativeDiagram.py FunctionToCoefficientCommutativeDiagram -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class FunctionToCoefficientCommutativeDiagram(InteractiveScene):
    def construct(self):
        # Axes
        axes1, axes2, axes3 = all_axes = VGroup(*(
            Axes((-3, 3), (-2, 4), width=6, height=4)
            for x in range(3)
        ))

        all_axes.arrange(RIGHT, buff=1.0)
        axes3.shift(4 * RIGHT)
        all_axes.set_width(FRAME_WIDTH - 1)
        all_axes.move_to(UP)

        # Graphs
        def p1(x):
            return 0.2 * (x + 3) * x * (x - 2)

        def p2(x):
            return -0.1 * (x + 2) * (x - 2) * (x - 3)

        graphs = VGroup(
            axes1.get_graph(p1).set_stroke(BLUE),
            axes2.get_graph(p2).set_stroke(TEAL),
            axes3.get_graph(lambda x: p1(x) * p2(x)).set_stroke(YELLOW),
        )
        graphs.set_stroke(width=2)

        kw = dict(font_size=30)
        graph_labels = VGroup(*(
            Tex(tex, **kw).next_to(axes.get_top(), RIGHT, aligned_edge=UP)
            for tex, axes in zip(["f(x)", "g(x)", R"f(x) \cdot g(x)"], all_axes)
        ))

        # Coefficients
        a_labels, b_labels, conv_label = coef_labels = VGroup(
            Tex(R"(a_0, a_1, \dots, a_n)", **kw),
            Tex(R"(b_0, b_1, \dots, b_m)", **kw),
            VGroup(
                Tex("c_0 = a_0 b_0", **kw),
                Tex("c_1 = a_0 b_1 + a_1 b_0", **kw),
                Tex("c_2 = a_0 b_2 + a_1 b_1 + a_2 b_0", **kw),
                Tex("c_3 = a_0 b_3 + a_1 b_2 + a_2 b_1 + a_3 b_0", **kw),
                Tex(R"\vdots", **kw),
            ).arrange(DOWN, aligned_edge=LEFT).scale(0.85)
        )
        v_arrows = VGroup()
        for labels, graph, axes in zip(coef_labels, graphs, all_axes):
            arrow = Vector(0.8 * DOWN)
            arrow.next_to(axes, DOWN)
            v_arrows.add(arrow)
            labels.next_to(arrow, DOWN)
            labels.match_color(graph)

            arrow_label = Text("Coefficients", font_size=24)
            arrow_label.next_to(arrow, RIGHT, buff=0.2)
            arrow.add(arrow_label)

        conv_label.to_edge(RIGHT, buff=SMALL_BUFF)

        # Operations
        mult_arrow = Arrow(axes2, axes3, buff=0.1, stroke_width=6)
        mult_arrow_label = Text("Multiplication", font_size=30)
        mult_arrow_label.next_to(mult_arrow, UP, SMALL_BUFF)
        mult_arrow = VGroup(mult_arrow, mult_arrow_label)
        mult_arrow.set_color(RED)

        coef_rect = SurroundingRectangle(coef_labels[:2])
        coef_rect.set_stroke(GREY, 2)
        conv_arrow = Arrow(coef_rect, conv_label[0], buff=0.3, stroke_width=6)
        conv_arrow_label = Text("Convolution", font_size=30)
        conv_arrow_label.next_to(conv_arrow, DOWN, SMALL_BUFF)
        conv_arrow = VGroup(conv_arrow, conv_arrow_label)
        conv_arrow.set_color(RED)

        # Animations
        self.play(
            LaggedStartMap(ShowCreation, graphs[:2]),
            LaggedStartMap(FadeIn, graph_labels[:2]),
            LaggedStartMap(FadeIn, all_axes[:2]),
        )
        self.play(LaggedStart(
            Write(mult_arrow, run_time=1),
            TransformFromCopy(graphs[0], graphs[2].copy(), remover=True),
            TransformFromCopy(graphs[1], graphs[2]),
            TransformFromCopy(all_axes[0], all_axes[2].copy(), remover=True),
            TransformFromCopy(all_axes[1], all_axes[2]),
            TransformFromCopy(graph_labels[0], graph_labels[2][:5]),
            TransformFromCopy(graph_labels[1], graph_labels[2][5:]),
        ), lag_ratio=0.2)
        self.wait()
        self.play(
            LaggedStartMap(Write, v_arrows[:2], lag_ratio=0.7),
            LaggedStartMap(FadeIn, coef_labels[:2], shift=DOWN, lag_ratio=0.7),
        )
        self.wait()
        self.play(ShowCreation(coef_rect), FadeIn(conv_arrow))
        self.play(
            FadeTransformPieces(a_labels.copy(), conv_label),
            FadeTransformPieces(b_labels.copy(), conv_label),
        )

        # Pointwise product
        all_dots = Group(*(
            Group(*(
                GlowDot(axes.i2gp(x, graph), radius=0.1, glow_factor=0.8, color=WHITE)
                for x in range(-3, 4)
            ))
            for axes, graph in zip(all_axes, graphs)
        ))
        all_circles = VGroup(*(
            VGroup(*(
                Circle(radius=0.1).set_stroke(YELLOW, 2).move_to(dot)
                for dot in dots
            ))
            for dots in all_dots
        ))
        self.play(
            LaggedStartMap(FadeIn, all_dots[0], scale=0.5, lag_ratio=0.5),
            LaggedStartMap(FadeIn, all_dots[1], scale=0.5, lag_ratio=0.5),
        )
        self.wait()
        self.play(
            ShowSubmobjectsOneByOne(all_circles[0]),
            ShowSubmobjectsOneByOne(all_circles[1]),
            ShowSubmobjectsOneByOne(all_circles[2]),
            ShowIncreasingSubsets(all_dots[2]),
            run_time=4,
            rate_func=linear,
        )
        self.remove(all_circles)
        self.wait()
        self.play(Write(v_arrows[2]))
        self.wait()
