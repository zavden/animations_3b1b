# ==============================================================================
# Scene:      TickingClock
# Source:     videos/_2018/WindingNumber_G.py (lines 2964-2985)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl TickingClock.py TickingClock -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/WindingNumber.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7


# This turns counterclockwise revs into their color. Beware, we use CCW angles 
# in all display code, but generally think in this video's script in terms of 
# CW angles
def rev_to_rgba(alpha):
    alpha = (0.5 - alpha) % 1 # For convenience, to go CW from red on left instead of CCW from right
    # 0 is red, 1/6 is yellow, 1/3 is green, 2/3 is blue
    hue_list = [0, 0.5/6.0, 1/6.0, 1.1/6.0, 2/6.0, 3/6.0, 4/6.0, 5/6.0]
    num_hues = len(hue_list)
    start_index = int(np.floor(num_hues * alpha)) % num_hues
    end_index = (start_index + 1) % num_hues
    beta = (alpha % (1.0/num_hues)) * num_hues

    start_hue = hue_list[start_index]
    end_hue = hue_list[end_index]
    if end_hue < start_hue:
        end_hue = end_hue + 1
    hue = interpolate(start_hue, end_hue, beta)

    return color_to_rgba(Color(hue = hue, saturation = 1, luminance = 0.5))


def rev_to_color(alpha):
    return rgba_to_color(rev_to_rgba(alpha))



# ----- From _2018/WindingNumber_G.py -----

class TickingClock(Scene):
    CONFIG = {
        "run_time" : 90,
    }
    def construct(self):
        clock = Clock()
        clock.set_height(FRAME_HEIGHT - 1)
        clock.to_edge(LEFT)
        lines = [clock.hour_hand, clock.minute_hand]
        def update_line(line):
            rev = line.get_angle()/TAU
            line.set_color(rev_to_color(rev))

        for line in lines:
            self.add(Mobject.add_updater(line, update_line))

        run_time = self.run_time
        self.play(ClockPassesTime(
            clock, 
            run_time = run_time,
            hours_passed = 0.1*run_time
        ))
