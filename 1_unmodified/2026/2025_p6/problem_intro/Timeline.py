# ==============================================================================
# Scene:      Timeline
# Source:     videos/_2026/2025_p6/problem_intro.py (lines 267-304)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Timeline.py Timeline -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Timeline(InteractiveScene):
    def construct(self):
        timeline = NumberLine(
            (2017, 2030, 1 / 12),
            unit_size=4,
            tick_size=0.1,
            longer_tick_multiple=2,
            big_tick_spacing=1,
        )
        timeline.set_y(-2)
        year_labels = timeline.add_numbers(
            range(2017, 2030),
            group_with_commas=False,
        )

        def update_year_label(label):
            year = label.get_value()
            label.next_to(timeline.n2p(year), DOWN, 0.4)
            focal_value = np.exp(-0.2 * label.get_x()**2)
            label.set_height(
                0.25 + 0.25 * focal_value,
                about_edge=UP
            )
            label.set_fill(opacity=(0.5 + 0.5 * focal_value))

        for label in year_labels:
            label.add_updater(update_year_label)

        def center_on_year(year, run_time=2):
            shift_value = timeline.n2p(year)[0] * LEFT
            return timeline.animate(run_time=run_time).shift(shift_value)

        self.add(timeline)
        self.play(center_on_year(2026))
        self.wait()
        self.play(center_on_year(2023))
        self.wait()
        self.play(center_on_year(2025))
