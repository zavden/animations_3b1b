# ==============================================================================
# Scene:      SphereExamplePointsDecimal
# Source:     videos/_2018/quaternions.py (lines 3288-3357)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SphereExamplePointsDecimal.py SphereExamplePointsDecimal -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SphereExamplePointsDecimal(Scene):
    CONFIG = {
        "point_rotation_angle_axis_pairs": [
            (45 * DEGREES, DOWN),
            (120 * DEGREES, OUT),
            (35 * DEGREES, rotate_vector(RIGHT, 30 * DEGREES)),
            (90 * DEGREES, IN),
        ]
    }

    def construct(self):
        decimals = VGroup(*[
            DecimalNumber(
                0,
                num_decimal_places=3,
                color=color,
                include_sign=True,
                edge_to_fix=RIGHT,
            )
            for color in [YELLOW, GREEN, RED]
        ])
        number_label = VGroup(
            decimals[0], OldTex("+"),
            decimals[1], OldTex("i"), OldTex("+"),
            decimals[2], OldTex("j"),
        )
        number_label.arrange(RIGHT, buff=SMALL_BUFF)
        number_label.to_corner(UL)

        point = VectorizedPoint(OUT)

        def generate_decimal_updater(decimal, index):
            shifted_i = (index - 1) % 3
            decimal.add_updater(lambda d: d.set_value(
                point.get_location()[shifted_i]
            ))
            return decimal

        for i, decimal in enumerate(decimals):
            self.add(generate_decimal_updater(decimal, i))

        decimal_braces = VGroup()
        for decimal, char in zip(decimals, "wxy"):
            brace = Brace(decimal, DOWN, buff=SMALL_BUFF)
            label = brace.get_tex(char, buff=SMALL_BUFF)
            label.match_color(decimal)
            brace.add(label)
            decimal_braces.add(brace)

        equation = OldTex(
            "w^2 + x^2 + y^2 = 1",
            tex_to_color_map={
                "w": YELLOW,
                "x": GREEN,
                "y": RED,
            }
        )
        equation.next_to(decimal_braces, DOWN, MED_LARGE_BUFF)

        self.add(number_label)
        self.add(decimal_braces)
        self.add(equation)

        pairs = self.point_rotation_angle_axis_pairs
        for angle, axis in pairs:
            self.play(
                Rotate(point, angle, axis=axis, about_point=ORIGIN),
                run_time=2
            )
            self.wait()
