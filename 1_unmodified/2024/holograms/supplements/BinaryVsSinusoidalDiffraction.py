# ==============================================================================
# Scene:      BinaryVsSinusoidalDiffraction
# Source:     videos/_2024/holograms/supplements.py (lines 974-1065)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BinaryVsSinusoidalDiffraction.py BinaryVsSinusoidalDiffraction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BinaryVsSinusoidalDiffraction(InteractiveScene):
    def construct(self):
        # Add axes
        top_axes, low_axes = two_axes = VGroup(
            Axes((0, 4, 0.5), (0, 1, 0.5), width=6, height=1.5)
            for _ in range(2)
        )
        two_axes.arrange(DOWN, buff=2.0)
        two_axes.to_edge(LEFT, buff=1.5)

        for axes in two_axes:
            y_label = Text("Opacity", font_size=30)
            y_label.next_to(axes.y_axis, UP, buff=MED_SMALL_BUFF)
            axes.add(y_label)
            axes.y_axis.add_numbers(font_size=16, num_decimal_places=1)

        self.add(two_axes)

        # Add graphs
        discontinuities = [*np.arange(5), *(np.arange(5) + 0.2)]
        discontinuities.sort()
        top_graph = top_axes.get_graph(self.func1, x_range=(0, 3.99), discontinuities=discontinuities)
        top_graph.set_stroke(TEAL, 2)

        low_axes.num_sampled_graph_points_per_tick = 20
        low_graph = low_axes.get_graph(self.func2)
        low_graph.set_stroke(BLUE, 2)

        graphs = VGroup(top_graph, low_graph)

        # Add gratings
        top_grating = self.get_grating(top_axes, self.func1, 1000)
        low_grating = self.get_grating(low_axes, self.func2, 1000)
        gratings = VGroup(top_grating, low_grating)

        # Animate in
        graphs.set_stroke(width=1)
        self.add(graphs)
        for graph, grating in [(top_graph, top_grating), (low_graph, low_grating)]:
            self.add(grating, graph)
            self.play(
                graph.animate.set_stroke(width=2),
                VShowPassingFlash(graph.copy().set_stroke(width=5), time_width=3, rate_func=linear),
                # ShowCreation(graph, rate_func=linear),
                FadeIn(grating, lag_ratio=1e-3),
                run_time=2
            )
            self.play(
                grating.animate.next_to(grating, RIGHT, MED_LARGE_BUFF),
                run_time=2
            )
            self.wait()

        # Labels
        high_beam_labels = VGroup(
            Text("Higher order beams", font_size=36).next_to(grating, UP)
            for grating in gratings
        )
        check = Checkmark().set_color(GREEN).scale(1.5)
        check.next_to(high_beam_labels[0])
        ex = Exmark().set_color(RED).scale(1.5)
        ex.next_to(high_beam_labels[1])

        self.play(LaggedStart(
            FadeIn(high_beam_labels),
            Write(check),
            Write(ex),
            lag_ratio=0.5
        ))
        self.wait()

    def get_grating(self, axes, func, n_slits):
        grating = Rectangle().replicate(n_slits)
        grating.set_stroke(width=0)
        grating.set_fill(GREY_D)
        grating.set_shading(0.25, 0.25, 0)
        grating.arrange(RIGHT, buff=0)
        grating.set_shape(axes.x_axis.get_width(), axes.y_axis.get_height())
        grating.move_to(axes.c2p(0, 0), DL)

        for mob in grating:
            mob.set_opacity(func(axes.x_axis.p2n(mob.get_center())))

        # grating.next_to(grating, RIGHT, MED_LARGE_BUFF)

        return grating

    def func1(self, x):
        return 0 if x % 1 < 0.2 else 1

    def func2(self, x):
        return math.sin(TAU * x)**2
