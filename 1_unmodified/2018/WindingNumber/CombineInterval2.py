# ==============================================================================
# Scene:      CombineInterval2
# Source:     videos/_2018/WindingNumber.py (lines 2341-2375)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CombineInterval2.py CombineInterval2 -w -m --fps 15
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


positive_color = rev_to_color(0)


class CombineInterval2(Scene):
    def construct(self):
        plus_sign = OldTex("+", fill_color = positive_color)

        def make_interval(a, b):
            line = Line(a, b)
            start_dot = Dot(a, color = positive_color)
            end_dot = Dot(b, color = positive_color)
            start_sign = plus_sign.copy().next_to(start_dot, UP)
            end_sign = plus_sign.copy().next_to(end_dot, UP)
            return Group(start_sign, end_sign, line, start_dot, end_dot)

        def pair_indicate(a, b):
            self.play(
                CircleIndicate(a),
                CircleIndicate(b)
            )

        left_interval = make_interval(2 * LEFT, LEFT)
        right_interval = make_interval(RIGHT, 2 * RIGHT)

        self.play(FadeIn(left_interval), FadeIn(right_interval))

        pair_indicate(left_interval[0], left_interval[1])

        pair_indicate(right_interval[0], right_interval[1])

        self.play(
            ApplyMethod(left_interval.shift, RIGHT),
            ApplyMethod(right_interval.shift, LEFT),
        )

        pair_indicate(left_interval[0], right_interval[1])

        self.wait()
