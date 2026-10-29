# ==============================================================================
# Scene:      BaselThumbnail
# Source:     videos/outside_videos/misc_thumbnails.py (lines 94-159)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BaselThumbnail.py BaselThumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Lighthouse is no longer exported from manim_imports_ext; it is imported from once_useful_constructs.light (as _2018/wallis.py does)
# ==============================================================================

# CHANGE: Lighthouse is no longer exported from manim_imports_ext; it is imported from once_useful_constructs.light (as _2018/wallis.py does)
from manim_imports_ext import *
from once_useful_constructs.light import Lighthouse

class BaselThumbnail(Scene):
    def construct(self):
        # Lake
        lake_radius = 6
        lake_center = ORIGIN

        lake = Circle(
            fill_color=BLUE,
            fill_opacity=0.0,
            radius=lake_radius,
            stroke_color=BLUE_D,
            stroke_width=3,
        )
        lake.move_to(lake_center)

        R = 2
        light_template = VGroup()
        rs = np.linspace(0, 1, 100)
        for r1, r2 in zip(rs, rs[1:]):
            dot1 = Dot(radius=R * r1).flip()
            dot2 = Dot(radius=R * r2)
            dot2.append_vectorized_mobject(dot1)
            dot2.insert_n_curves(100)
            dot2.set_fill(YELLOW, opacity=0.5 * (1 - r1)**2)
            dot2.set_stroke(width=0)
            light_template.add(dot2)

        houses = VGroup()
        lights = VGroup()
        for i in range(16):
            theta = -TAU / 4 + (i + 0.5) * TAU / 16
            pos = lake_center + lake_radius * np.array([np.cos(theta), np.sin(theta), 0])
            house = Lighthouse()
            house.set_fill(GREY_B)
            house.set_stroke(width=0)
            house.set_height(0.5)
            house.move_to(pos)
            light = light_template.copy()
            light.move_to(pos)
            houses.add(house)
            lights.add(light)

        self.add(lake)
        self.add(houses)
        self.add(lights)

        # Equation
        equation = OldTex(
            "1", "+", "{1 \\over 4}", "+",
            "{1 \\over 9}", "+", "{1 \\over 16}", "+",
            "{1 \\over 25}", "+", "\\cdots"
        )
        equation.scale(1.8)
        equation.move_to(2 * UP)
        answer = OldTex("= \\frac{\\pi^2}{6}", color=YELLOW)
        answer.scale(3)
        answer.move_to(1.25 * DOWN)
        equation.add(answer)

        shadow = VGroup()
        for w in np.linspace(20, 0, 50):
            shadow.add(equation.copy().set_fill(opacity=0).set_stroke(BLACK, width=w, opacity=0.02))
        self.add(shadow)
        self.add(equation)

        self.wait()
