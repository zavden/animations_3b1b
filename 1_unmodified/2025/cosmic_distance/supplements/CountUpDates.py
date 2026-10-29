# ==============================================================================
# Scene:      CountUpDates
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 1166-1196)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CountUpDates.py CountUpDates -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CountUpDates(InteractiveScene):
    def construct(self):
        # Test
        day_tracker = ValueTracker(1)
        label = always_redraw(lambda: self.day_to_date_label(int(day_tracker.get_value())))
        self.add(label)
        self.play(
            day_tracker.animate.set_value(365),
            run_time=10,
            rate_func=smooth
        )

    def day_to_date_label(self, day_number, buff=MED_SMALL_BUFF):
        # Days in each month (non-leap year)
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        # Find the month
        month = 0
        days_remaining = day_number
        while days_remaining > month_days[month]:
            days_remaining -= month_days[month]
            month += 1

        result = VGroup(
            Text(month_names[month]),
            Integer(days_remaining),
        )
        result.arrange(RIGHT, buff=buff, aligned_edge=UP)
        result[0].set_y(result[1].get_y(DOWN) - result[0][0].get_y(DOWN))
        result.shift(-result[1].get_left())
        return result
