# ==============================================================================
# Scene:      RandomVectorStatistics
# Source:     videos/_2024/puzzles/added_dimension.py (lines 2784-2883)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomVectorStatistics.py RandomVectorStatistics -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RandomVectorStatistics(InteractiveScene):
    def construct(self):
        # Show 2d distribution
        chart = self.get_random_angle_data_histogram(2, step_size=2)

        label = VGroup(Integer(2, edge_to_fix=UR), Text("D"))
        label.arrange(RIGHT, buff=0.05)
        label.next_to(chart.get_corner(UL), DR)
        label.shift(RIGHT)

        self.add(label)
        self.add(chart)

        # Many random vectors
        center = chart.get_center() + 0.5 * UP
        for _ in range(0):
            vects = VGroup(
                Vector(
                    1.5 * rotate_vector(RIGHT, random.uniform(0, TAU)),
                    thickness=4
                ).set_fill(random_bright_color(), border_width=1)
                for _ in range(2)
            )
            vects.shift(center)
            angle = (vects[0].get_angle() - vects[1].get_angle()) % TAU
            if angle > PI:
                angle = TAU - angle

            bar = chart.bars[int(angle / DEGREES) // 2].copy()
            bar.set_color(YELLOW)

            self.add(vects, bar)
            self.wait(0.5)
            self.remove(vects, bar)

        # Animate an increase in charts
        dim_tracker = ValueTracker(2)

        def get_dim():
            return int(dim_tracker.get_value())

        label.add_updater(lambda m: m[0].set_value(get_dim()))

        self.play(
            dim_tracker.animate.set_value(1000).set_anim_args(rate_func=rush_into),
            UpdateFromFunc(chart, lambda m: m.become(
                self.get_random_angle_data_histogram(
                    get_dim(),
                    n_vects=50000000 // get_dim(),
                    # n_vects=500000 // get_dim(),
                    step_size=1 if get_dim() < 100 else 0.5
                )
            )),
            run_time=20
        )

    def get_random_angle_data_histogram(self, dim, n_vects=1000000, step_size=1):
        vects1, vects2 = all_vects = [np.random.normal(0, 1, (n_vects, dim)) for _ in range(2)]

        for vects in all_vects:
            norms = np.linalg.norm(vects, axis=1)
            vects /= norms[:, np.newaxis]

        angles = np.arccos((vects1 * vects2).sum(1)) / DEGREES

        return self.get_histogram(angles, step_size=step_size)

    def get_histogram(self, data, min_val=0, max_val=180, step_size=5, bar_color=BLUE_D):
        bins = np.arange(min_val, max_val + 1, step_size)
        bucket_counts, _ = np.histogram(data, bins=bins, range=(min_val, max_val))

        bin_width = step_size / (max_val - min_val)
        densities = (bucket_counts / bucket_counts.sum()) / (bin_width)

        y_max = 16.0
        if densities.max() > y_max:
            densities *= (y_max / densities.max())**0.5

        axes = Axes(
            x_range=(min_val, max_val, 5),
            y_range=(0, y_max, 2),  # TODO
            width=6, height=4
        )
        axes.x_axis.add_numbers(np.arange(min_val, max_val + 1, 45), font_size=24, unit_tex=R"^\circ")
        x_unit = axes.x_axis.get_unit_size()
        y_unit = axes.y_axis.get_unit_size()

        bar_width = x_unit * step_size

        bars = VGroup(
            Rectangle(width=bar_width, height=density * y_unit).move_to(axes.c2p(x, 0), DL)
            for x, density in zip(bins, densities)
        )
        bars.set_fill(bar_color, 1)
        bars.set_stroke(WHITE, 0.5, 0.5)

        chart = VGroup(axes, bars)
        chart.axes = axes
        chart.bars = bars
        return chart
