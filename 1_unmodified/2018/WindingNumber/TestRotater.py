# ==============================================================================
# Scene:      TestRotater
# Source:     videos/_2018/WindingNumber.py (lines 1342-1348)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TestRotater.py TestRotater -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath

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


class FuncRotater(Animation):
    CONFIG = {
        "rev_func" : lambda x : x, # Func from alpha to CCW revolutions,
    }

    # Perhaps abstract this out into an "Animation updating from original object" class
    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        submobject.set_points(starting_submobject.get_points())

    def interpolate_mobject(self, alpha):
        Animation.interpolate_mobject(self, alpha)
        angle_revs = self.rev_func(alpha)
        self.mobject.rotate(
            angle_revs * TAU, 
            about_point = ORIGIN
        )
        self.mobject.set_color(rev_to_color(angle_revs))


class TestRotater(Scene):
    def construct(self):
        test_line = Line(ORIGIN, RIGHT)
        self.play(FuncRotater(
            test_line,
            rev_func = lambda x : x % 0.25,
            run_time = 10))
