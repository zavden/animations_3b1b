# ==============================================================================
# Scene:      MultipleBellishCurves
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 44-164)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MultipleBellishCurves.py MultipleBellishCurves -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MultipleBellishCurves(InteractiveScene):
    def construct(self):
        # Axes
        line_style = dict(stroke_color=GREY_B, stroke_width=1)
        faded_line_style = dict(stroke_opacity=0.25, **line_style)
        all_axes = VGroup(*(
            NumberPlane(
                (-3, 3), (0, 1, 0.5),
                height=1.5, width=4,
                background_line_style=line_style,
                faded_line_style=faded_line_style,
            )
            for _ in range(3)
        ))
        all_axes.arrange(DOWN, buff=LARGE_BUFF)
        all_axes.to_edge(LEFT)

        # Graphs
        def pseudo_bell(x):
            A = np.abs(x) + np.exp(-1)
            return np.exp(-np.exp(-1)) * A**(-A)

        graphs = VGroup(
            all_axes[0].get_graph(lambda x: np.exp(-x**2)),
            all_axes[1].get_graph(lambda x: 1 / (1 + x**2)),
            all_axes[2].get_graph(pseudo_bell),
        )
        labels = VGroup(
            Tex("e^{-x^2}"),
            Tex(R"\frac{1}{1 + x^2}"),
            Tex(
                R"e^{-1 / e}\left(|x|+\frac{1}{e}\right)^{-\left(|x|+\frac{1}{e}\right)}",
                font_size=40
            ),
        )

        plots = VGroup()
        colors = color_gradient([YELLOW, RED], 3)
        for axes, label, graph, color in zip(all_axes, labels, graphs, colors):
            label.next_to(axes, RIGHT)
            graph.set_stroke(color, 3)
            plots.add(VGroup(axes, graph))

        # Show initial graph
        plot = plots[0]
        plot.save_state()
        plot.center()
        plot.set_height(4)
        label = labels[0]
        label.save_state()
        label.set_height(1.25)
        label.next_to(plot.get_corner(UR), DL)
        words = Text("Normal Distribution (aka Gaussian)", font_size=60)
        words.next_to(plot, UP, MED_LARGE_BUFF)
        words.save_state()
        normal = words["Normal Distribution"]
        gaussian = words["(aka Gaussian)"]
        gaussian.set_opacity(0)
        normal.set_x(0)
        gaussian.set_x(0)

        self.add(plot)
        self.add(words)
        graph_copy = plot[1].copy()
        self.play(UpdateFromAlphaFunc(
            plot[1], lambda m, a: m.pointwise_become_partial(
                graph_copy, 0.5 - 0.5 * a, 0.5 + 0.5 * a
            ),
            run_time=2,
        ))
        self.play(words.animate.restore())
        self.wait()
        self.play(
            Write(label),
            VShowPassingFlash(
                graph_copy.set_stroke(YELLOW, width=10),
                time_width=2,
                run_time=3,
            ),
        )
        self.wait()

        # Ask why
        question = Text("Why this function?", font_size=60)
        arrow = Vector(LEFT)
        arrow.next_to(label.saved_state, RIGHT)
        question.next_to(arrow, RIGHT)
        self.play(
            plot.animate.restore(),
            label.animate.restore(),
            words.animate.match_width(plot.saved_state).next_to(plot.saved_state, UP, SMALL_BUFF),
            GrowArrow(arrow),
            FadeIn(question, lag_ratio=0.1, shift=0.2 * LEFT),
        )
        self.wait()

        last_plot = plot
        last_label = label
        for plot, label in zip(plots[1:], labels[1:]):
            self.play(
                TransformFromCopy(last_plot, plot),
                TransformMatchingTex(last_label.copy(), label, run_time=1),
            )
            self.wait()
            last_plot = plot
            last_label = label
        self.wait()

        # Highlight first function
        l0 = labels[0]
        l0.generate_target()
        l0.target.set_height(1.0, about_edge=DL)
        l0.target.shift(0.1 * RIGHT)
        self.play(LaggedStart(
            MoveToTarget(l0),
            VGroup(arrow, question).animate.next_to(l0.target, RIGHT, aligned_edge=DOWN),
            labels[1:].animate.fade(0.5),
            plots[1:].animate.fade(0.5),
            FlashAround(l0.target, time_width=1.5),
        ))
        self.wait()
