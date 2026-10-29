# ==============================================================================
# Scene:      SignsExplanation
# Source:     videos/_2018/WindingNumber.py (lines 1503-1535)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SignsExplanation.py SignsExplanation -w -m --fps 15
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


class SignsExplanation(Scene):
    def construct(self):
        num_line = NumberLine()
        largest_num = 10
        num_line.add_numbers(*list(range(-largest_num, largest_num + 1)))
        self.add(num_line)
        self.wait()

        pos_num = 3
        neg_num = -pos_num

        pos_arrow = Arrow(
                num_line.number_to_point(0), 
                num_line.number_to_point(pos_num),
                buff = 0,
                color = positive_color)
        neg_arrow = Arrow(
                num_line.number_to_point(0), 
                num_line.number_to_point(neg_num),
                buff = 0,
                color = negative_color)

        plus_sign = OldTex("+", fill_color = positive_color)
        minus_sign = OldTex("-", fill_color = negative_color)

        plus_sign.next_to(pos_arrow, UP)
        minus_sign.next_to(neg_arrow, UP)
        
        #num_line.add_numbers(pos_num)
        self.play(ShowCreation(pos_arrow), FadeIn(plus_sign))

        #num_line.add_numbers(neg_num)
        self.play(ShowCreation(neg_arrow), FadeIn(minus_sign))
