# ==============================================================================
# Scene:      LongerDuration
# Source:     videos/_2025/cosmic_distance/part2.py (lines 203-205)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LongerDuration.py LongerDuration -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowDuration(InteractiveScene):
    max_time = 4 * 3600 + 20 * 20 + 35
    run_time = 12
    clock_color = BLACK

    def construct(self):
        # Increment clock
        clock = VGroup(
            Integer(0, min_total_width=2),
            Text("h"),
            Integer(0, min_total_width=2),
            Text("m"),
            Integer(0, min_total_width=2),
            Text("s"),
        )
        clock.arrange(RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
        clock[1::2].shift(0.5 * SMALL_BUFF * LEFT)

        clock.set_fill(self.clock_color)
        self.add(clock)

        time_tracker = ValueTracker()

        def update_clock(clock):
            time = int(time_tracker.get_value())  # In seconds
            clock[4].set_value(time % 60)  # Seconds
            clock[2].set_value((time // 60) % 60)  # Minutes
            clock[0].set_value((time // 3600))  # Minutes

        clock.add_updater(update_clock)
        self.play(time_tracker.animate.set_value(self.max_time), rate_func=linear, run_time=self.run_time)
        self.wait()


class LongerDuration(ShowDuration):
    max_time = 4 * 3600 + 20 * 20 + 35
    run_time = 12
