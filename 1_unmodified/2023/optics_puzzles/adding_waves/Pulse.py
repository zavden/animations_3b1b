# ==============================================================================
# Scene:      Pulse
# Source:     videos/_2023/optics_puzzles/adding_waves.py (lines 1027-1106)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Pulse.py Pulse -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Pulse(InteractiveScene):
    def construct(self):
        # Setup axes
        n_parts = 10
        x_max = 4
        left_axes_group = VGroup(*(
            Axes(
                (0, x_max), (-1, 1),
                width=0.5 * FRAME_WIDTH - 2,
                height=1,
                num_sampled_graph_points_per_tick=20,
            )
            for _ in range(n_parts)
        ))
        left_axes_group.arrange(DOWN, buff=0.75)
        left_axes_group.set_height(FRAME_HEIGHT - 1)
        left_axes_group.to_edge(LEFT)

        right_axes = Axes((0, x_max), (-1, 1), width=0.5 * FRAME_WIDTH - 1, height=3)
        right_axes.to_edge(RIGHT)

        brace = Brace(left_axes_group, RIGHT, buff=0.5)
        arrow = Arrow(brace, right_axes)
        sigma = Tex(R"\Sigma", font_size=72).next_to(arrow, UP)

        self.add(left_axes_group)
        self.add(right_axes)
        self.add(brace, arrow, sigma)

        # Graphs
        f0 = 6
        sigma = 2
        frequencies = np.linspace(0, 2 * f0, n_parts + 1)[1:]
        weights = 0.25 * np.exp(-0.5 * ((frequencies - f0) / sigma) ** 2)
        speeds = np.linspace(8, 10, n_parts)
        time_tracker = ValueTracker(0)
        colors = color_gradient([BLUE, YELLOW], n_parts)

        left_graphs = VGroup(*(
            self.create_graph(axes, freq, speed, color, time_tracker)
            for axes, freq, speed, color in zip(
                left_axes_group,
                frequencies,
                speeds,
                colors,
            )
        ))

        def sum_func(x):
            time = time_tracker.get_value()
            return sum(
                weight * self.wave_func(x, freq, speed, time)
                for weight, freq, speed in zip(weights, frequencies, speeds)
            )

        sum_graph = right_axes.get_graph(sum_func, bind=True)
        sum_graph.set_stroke(TEAL, 3)

        self.add(left_graphs)
        self.add(sum_graph)

        final_time = 20.0
        time_tracker.set_value(0)
        self.play(
            time_tracker.animate.increment_value(final_time),
            rate_func=linear,
            run_time=final_time,
        )


    def wave_func(self, x, freq, speed, time):
        return np.cos(freq * x - speed * time)

    def create_graph(self, axes, freq, speed, color, time_tracker):
        return axes.get_graph(
            lambda x: self.wave_func(x, freq, speed, time_tracker.get_value()),
            stroke_color=color,
            stroke_width=2,
            bind=True
        )
