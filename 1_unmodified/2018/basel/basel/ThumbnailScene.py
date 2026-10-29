# ==============================================================================
# Scene:      ThumbnailScene
# Source:     videos/_2018/basel/basel.py (lines 4335-4377)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThumbnailScene.py ThumbnailScene -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


LIGHT_COLOR = YELLOW


LIGHT_COLOR = YELLOW


LAKE_COLOR = BLUE


LAKE_OPACITY = 0.15


LAKE_STROKE_WIDTH = 5.0


LAKE_STROKE_COLOR = BLUE


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint,scale,cutoff: inverse_power_law(maxint,scale,cutoff,2)


class ThumbnailScene(Scene):

    def construct(self):

        equation = OldTex("1+{1\over 4}+{1\over 9}+{1\over 16}+{1\over 25}+\dots")
        equation.scale(1.5)
        equation.move_to(1.5 * UP)
        q_mark = OldTex("=?", color = LIGHT_COLOR).scale(5)
        q_mark.next_to(equation, DOWN, buff = 1.5)
        #equation.move_to(2 * UP)
        #q_mark = OldTex("={\pi^2\over 6}", color = LIGHT_COLOR).scale(3)
        #q_mark.next_to(equation, DOWN, buff = 1)

        lake_radius = 6
        lake_center = ORIGIN
        op_scale = 0.4

        lake = Circle(
            fill_color = LAKE_COLOR, 
            fill_opacity = LAKE_OPACITY, 
            radius = lake_radius,
            stroke_color = LAKE_STROKE_COLOR, 
            stroke_width = LAKE_STROKE_WIDTH,
        )
        lake.move_to(lake_center)

        for i in range(16):
            theta = -TAU/4 + (i + 0.5) * TAU/16
            pos = lake_center + lake_radius * np.array([np.cos(theta), np.sin(theta), 0])
            ls = LightSource(
                radius = 15.0, 
                num_levels = 150,
                max_opacity_ambient = 1.0,
                opacity_function = inverse_quadratic(1,op_scale,1)
            )
            ls.move_source_to(pos)
            lake.add(ls.ambient_light, ls.lighthouse)

        self.add(lake)

        self.add(equation, q_mark)

        self.wait()
