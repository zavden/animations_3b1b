# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2018/basel/basel2.py (lines 4567-4616)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
# ==============================================================================

# CHANGE: import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
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


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint, scale, cutoff: inverse_power_law(maxint,scale,cutoff,2)


class Thumbnail(Scene):
    CONFIG = {
        "light_source_config" : {
            "num_levels" : 250,
            "radius" : 10.0, 
            "max_opacity_ambient" : 1.0,
            "opacity_function" : inverse_quadratic(1,0.25,1)
        }
    }
    def construct(self):
        equation = OldTex(
            "1", "+", "{1\over 4}", "+", 
            "{1\over 9}","+", "{1\over 16}","+", 
            "{1\over 25}", "+", "\cdots"
        )
        equation.scale(1.8)
        equation.move_to(2*UP)
        equation.set_stroke(RED, 1)
        answer = OldTex("= \\frac{\\pi^2}{6}", color = LIGHT_COLOR)
        answer.scale(3)
        answer.set_stroke(RED, 1)
        # answer.next_to(equation, DOWN, buff = 1)
        answer.move_to(1.25*DOWN)
        #equation.move_to(2 * UP)
        #answer = OldTex("={\pi^2\over 6}", color = LIGHT_COLOR).scale(3)
        #answer.next_to(equation, DOWN, buff = 1)

        lake_radius = 6
        lake_center = ORIGIN

        lake = Circle(
            fill_color = BLUE, 
            fill_opacity = 0.15,
            radius = lake_radius,
            stroke_color = BLUE_D, 
            stroke_width = 3,
        )
        lake.move_to(lake_center)

        for i in range(16):
            theta = -TAU/4 + (i + 0.5) * TAU/16
            pos = lake_center + lake_radius * np.array([np.cos(theta), np.sin(theta), 0])
            ls = LightSource(**self.light_source_config)
            ls.move_source_to(pos)
            lake.add(ls.ambient_light)
            lake.add(ls.lighthouse)

        self.add(lake)
        self.add(equation, answer)
        self.wait()
