# ==============================================================================
# Scene:      ArrowCircleTest
# Source:     videos/_2018/WindingNumber.py (lines 1301-1322)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArrowCircleTest.py ArrowCircleTest -w -m --fps 15
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


class ArrowCircleTest(Scene):
    def construct(self):
        circle_radius = 3
        circle = Circle(radius = circle_radius, color = WHITE)
        self.add(circle)

        base_arrow = Arrow(circle_radius * 0.7 * RIGHT, circle_radius * 1.3 * RIGHT)

        def rev_rotate(x, revs):
            x.rotate(revs * TAU, about_point = ORIGIN)
            x.set_color(rev_to_color(revs))
            return x

        num_arrows = 8 * 3

        # 0.5 - fdiv below so as to get a clockwise rotation from left
        arrows = [rev_rotate(base_arrow.copy(), 0.5 - (fdiv(i, num_arrows))) for i in range(num_arrows)]
        arrows_vgroup = VGroup(*arrows)

        self.play(ShowCreation(arrows_vgroup), run_time = 2.5, rate_func=linear)

        self.wait()
