# ==============================================================================
# Scene:      BorderOf2dRegionScene
# Source:     videos/_2018/WindingNumber.py (lines 2423-2433)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BorderOf2dRegionScene.py BorderOf2dRegionScene -w -m --fps 15
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


# Useful constants to play around with
UL = UP + LEFT


UR = UP + RIGHT


DL = DOWN + LEFT


DR = DOWN + RIGHT


standard_rect = np.array([UL, UR, DR, DL])


# Used in EquationSolver2d, and a few other places
border_stroke_width = 10


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


negative_color = rev_to_color(0.5)


neutral_color = rev_to_color(0.25)


class BorderOf2dRegionScene(Scene):
    def construct(self):
        num_plane = NumberPlane()
        self.add(num_plane)

        points = standard_rect + 1.5 * UP + 2 * RIGHT
        interior = Polygon(*points, fill_color = neutral_color, fill_opacity = 1, stroke_width = 0)
        self.play(FadeIn(interior))

        border = Polygon(*points, color = negative_color, stroke_width = border_stroke_width)
        self.play(ShowCreation(border))
