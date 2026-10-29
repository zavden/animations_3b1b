# ==============================================================================
# Scene:      NumberLineScene
# Source:     videos/_2018/WindingNumber.py (lines 1671-1721)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NumberLineScene.py NumberLineScene -w -m --fps 15
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


class NumberLineScene(Scene):
    def construct(self):
        num_line = NumberLine()
        self.add(num_line)
        # TODO: Add labels, arrows, specific points
        self.wait()

        border_color = PURPLE_E
        inner_color = RED
        stroke_width = 10

        left_point = num_line.number_to_point(-1)
        right_point = num_line.number_to_point(1)
        # TODO: Make this line a thin rectangle
        interval_1d = Line(left_point, right_point, 
            stroke_color = inner_color, stroke_width = stroke_width)
        rect_1d = Rectangle(stroke_width = 0, fill_opacity = 1, fill_color = inner_color)
        rect_1d.replace(interval_1d)
        rect_1d.stretch_to_fit_height(SMALL_BUFF)
        left_dot = Dot(left_point, stroke_width = stroke_width, color = border_color)
        right_dot = Dot(right_point, stroke_width = stroke_width, color = border_color)
        endpoints_1d = VGroup(left_dot, right_dot)
        full_1d = VGroup(rect_1d, endpoints_1d)
        self.play(ShowCreation(full_1d))
        self.wait()

        # TODO: Can polish the morphing above; have dots become left and right sides, and 
        # only then fill in the top and bottom

        num_plane = NumberPlane()

        random_points = [UP + LEFT, UP + RIGHT, DOWN + RIGHT, DOWN + LEFT]

        border_2d = Polygon(
            *random_points,
            stroke_color = border_color,
            stroke_width = stroke_width)

        filling_2d = Polygon(
            *random_points,
            fill_color = inner_color,
            fill_opacity = 0.8,
            stroke_width = stroke_width)
        full_2d = VGroup(filling_2d, border_2d)

        self.play(
            FadeOut(num_line), 
            FadeIn(num_plane),
            ReplacementTransform(full_1d, full_2d))

        self.wait()
