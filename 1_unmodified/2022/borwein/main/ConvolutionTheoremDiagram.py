# ==============================================================================
# Scene:      ConvolutionTheoremDiagram
# Source:     videos/_2022/borwein/main.py (lines 1583-1760)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConvolutionTheoremDiagram.py ConvolutionTheoremDiagram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConvolutionTheoremDiagram(InteractiveScene):
    def construct(self):
        # Axes
        width = FRAME_WIDTH / 2 - 1
        height = 1.5
        left_axes = VGroup(*(
            Axes((-4, 4), (-0.5, 1, 0.5), width=width, height=height)
            for x in range(3)
        ))
        right_axes = VGroup(*(
            Axes((-1, 1, 0.5), (0, 1), width=width, height=2 * height / 3)
            for x in range(3)
        ))

        left_axes.arrange(DOWN, buff=1.0)
        left_axes[-1].to_edge(DOWN, buff=MED_SMALL_BUFF)
        left_axes.set_x(-FRAME_WIDTH / 4)
        for a1, a2 in zip(left_axes, right_axes):
            a2.shift(a1.get_origin() - a2.get_origin())
        right_axes.set_x(FRAME_WIDTH / 4)

        # Graphs
        left_graphs = VGroup(
            left_axes[0].get_graph(np.sinc, color=BLUE),
            left_axes[1].get_graph(lambda x: np.sinc(x / 2), color=YELLOW),
            left_axes[2].get_graph(lambda x: np.sinc(x) * np.sinc(x / 2), color=GREEN),
        )
        left_graphs.set_stroke(width=2)
        right_graphs = VGroup(
            VMobject().set_points_as_corners([
                right_axes[0].c2p(x, y) for x, y in [
                    (-1, 0), (-0.5, 0), (-0.5, 1),
                    (0.5, 1), (0.5, 0), (1, 0),
                ]
            ]).set_stroke(BLUE, 2),
            VMobject().set_points_as_corners([
                right_axes[1].c2p(x, y) for x, y in [
                    (-1, 0), (-0.5 / 2, 0), (-0.5 / 2, 2),
                    (0.5 / 2, 2), (0.5 / 2, 0), (1, 0),
                ]
            ]).set_stroke(YELLOW, 2),
            VMobject().set_points_as_corners([
                right_axes[2].c2p(x, y) for x, y in [
                    (-1, 0), (-0.75, 0), (-0.25, 1),
                    (0.25, 1), (0.75, 0), (1, 0),
                ]
            ]).set_stroke(GREEN, 2),
        )

        left_plots = VGroup(*(VGroup(axes, graph) for axes, graph in zip(left_axes, left_graphs)))
        right_plots = VGroup(*(VGroup(axes, graph) for axes, graph in zip(right_axes, right_graphs)))

        # Labels
        left_labels = VGroup(
            OldTex(R"\frac{\sin(\pi x)}{\pi x}")[0],
            OldTex(R"\frac{\sin(\pi x / 2)}{\pi x / 2}")[0],
            OldTex(R"\frac{\sin(\pi x)}{\pi x} \cdot \frac{\sin(\pi x / 2)}{\pi x / 2}")[0],
        )
        right_labels = VGroup(*(
            OldTex(
                Rf"\mathcal{{F}}\left[{ll.get_tex()}\right]",
                tex_to_color_map={R"\mathcal{F}": TEAL}
            )
            for ll in left_labels
        ))
        VGroup(left_labels, right_labels).scale(0.5)

        for label_group, axes_group, x in (left_labels, left_axes, -2), (right_labels, right_axes, -0.85):
            for label, axes in zip(label_group, axes_group):
                label.move_to(axes.c2p(x, 1))
        VGroup(left_labels[2], right_labels[2]).shift(0.5 * UP)

        ft_arrows = VGroup(*(
            Arrow(l1.get_right(), l2.get_left(), buff=0.2, path_arc=arc, color=TEAL, stroke_width=3)
            for l1, l2, arc in zip(left_labels, right_labels, (-0.3, -0.75, -1.0))
        ))

        # Left animations
        self.play(
            LaggedStartMap(FadeIn, left_plots[:2], lag_ratio=0.5),
            LaggedStartMap(FadeIn, left_labels[:2], lag_ratio=0.5),
            run_time=1
        )
        self.wait()
        self.play(
            Transform(left_plots[0].copy(), left_plots[2].copy(), remover=True),
            TransformFromCopy(left_plots[1], left_plots[2], remover=True),
            FadeTransform(left_labels[0].copy(), left_labels[2][:len(left_labels[0])]),
            FadeTransform(left_labels[1].copy(), left_labels[2][len(left_labels[0]):]),
        )
        self.add(left_plots[2])
        self.wait()
        self.play(
            ShowCreation(ft_arrows[2]),
            FadeTransform(left_labels[2].copy(), right_labels[2]),
            FadeIn(right_plots[2]),
        )
        self.wait()

        # Right animations
        for i in range(2):
            self.play(
                ShowCreation(ft_arrows[i]),
                FadeTransform(left_labels[i].copy(), right_labels[i]),
                FadeIn(right_plots[i]),
            )
        self.wait()

        right_labels[2].generate_target()
        equation = VGroup(
            right_labels[2].target,
            OldTex("=").scale(0.75),
            right_labels[0].copy(),
            OldTex("*").scale(0.75),
            right_labels[1].copy(),
        )
        equation.arrange(RIGHT, buff=SMALL_BUFF)
        equation.next_to(right_axes[2], UP, SMALL_BUFF)

        self.play(LaggedStart(
            ft_arrows[2].animate.put_start_and_end_on(
                ft_arrows[2].get_start(),
                right_labels[2].target.get_left() + SMALL_BUFF * UL,
            ),
            MoveToTarget(right_labels[2]),
            Write(equation[1]),
            FadeTransform(right_labels[0].copy(), equation[2]),
            Write(equation[3]),
            FadeTransform(right_labels[1].copy(), equation[4]),
            run_time=2
        ))

        # Show convolution
        x_unit = right_axes[1].x_axis.unit_size
        y_unit = right_axes[1].y_axis.unit_size
        rect = Rectangle(width=x_unit / 2, height=2 * y_unit)
        rect.set_stroke(YELLOW, 1)
        rect.set_fill(YELLOW, 0)
        rect.move_to(right_axes[1].get_origin(), DOWN)

        dot = GlowDot(color=GREEN)
        dot.move_to(right_graphs[2].get_start())

        self.add(rect, right_plots)
        self.play(
            rect.animate.move_to(right_axes[0].c2p(-1, 0), DOWN).set_fill(opacity=0.5),
            FadeIn(dot),
        )
        self.play(
            MoveAlongPath(dot, right_graphs[2]),
            UpdateFromFunc(rect, lambda m: m.match_x(dot)),
            run_time=8,
        )
        self.play(FadeOut(rect), FadeOut(dot))

        # Show signed area
        area = left_axes[2].get_riemann_rectangles(
            left_graphs[2],
            dx=0.01,
            colors=(BLUE_D, BLUE_D),
            fill_opacity=1.0,
        )
        o = area.get_center()
        area.sort(lambda p: abs(p[0] - o[0]))

        self.add(area, left_axes[2], left_graphs[2])
        self.play(Write(area, stroke_width=1, run_time=2))
        self.wait()
        rect.set_fill(opacity=0.2)
        rect.set_stroke(width=0)
        self.play(
            MoveAlongPath(dot, right_graphs[2], rate_func=lambda t: smooth(1 - 0.5 * t)),
            MoveAlongPath(dot.copy(), right_graphs[2], rate_func=lambda t: smooth(0.5 * t)),
            # UpdateFromFunc(rect, lambda m: m.match_x(dot)),
            run_time=1,
        )
        self.play(FlashAround(dot, buff=0, run_time=2, time_width=1))
        self.wait()
