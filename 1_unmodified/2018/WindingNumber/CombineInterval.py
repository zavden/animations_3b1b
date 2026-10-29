# ==============================================================================
# Scene:      CombineInterval
# Source:     videos/_2018/WindingNumber.py (lines 2287-2339)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CombineInterval.py CombineInterval -w -m --fps 15
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


negative_color = rev_to_color(0.5)


class CombineInterval(Scene):
    def construct(self):
        plus_sign = OldTex("+", fill_color = positive_color)
        minus_sign = OldTex("-", fill_color = negative_color)

        left_point = Dot(LEFT, color = positive_color)
        right_point = Dot(RIGHT, color = negative_color)
        line1 = Line(LEFT, RIGHT)
        interval1 = Group(line1, left_point, right_point)

        plus_sign.next_to(left_point, UP)
        minus_sign.next_to(right_point, UP)

        self.add(interval1, plus_sign, minus_sign)
        self.wait()
        self.play(
            CircleIndicate(plus_sign),
            CircleIndicate(minus_sign),
        )
        self.wait()

        mid_point = Dot(ORIGIN, color = GREY)

        question_mark = OldTex("?", fill_color = GREY)
        plus_sign_copy = plus_sign.copy()
        minus_sign_copy = minus_sign.copy()
        new_signs = Group(question_mark, plus_sign_copy, minus_sign_copy)
        for sign in new_signs: sign.next_to(mid_point, UP)

        self.play(FadeIn(mid_point), FadeIn(question_mark))
        self.wait()

        self.play(
            ApplyMethod(mid_point.set_color, positive_color),
            ReplacementTransform(question_mark, plus_sign_copy),
        )
        self.play(
            CircleIndicate(plus_sign_copy),
            CircleIndicate(minus_sign),
        )

        self.wait()

        self.play(
            ApplyMethod(mid_point.set_color, negative_color),
            ReplacementTransform(plus_sign_copy, minus_sign_copy),
        )
        self.play(
            CircleIndicate(minus_sign_copy),
            CircleIndicate(plus_sign),
        )

        self.wait()
