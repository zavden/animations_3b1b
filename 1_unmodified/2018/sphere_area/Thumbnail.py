# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2018/sphere_area.py (lines 3660-3708)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail(SpecialThreeDScene):
    CONFIG = {
        "camera_config": {
            "light_source_start_point": [-10, 5, 7],
        }
    }

    def construct(self):
        radius = 1.75
        sphere = self.get_sphere(radius=radius)
        sphere.rotate(70 * DEGREES, LEFT)
        sphere.set_fill(BLUE_E)
        sphere.set_stroke(WHITE, 0.5)

        circles = VGroup(*[
            Circle(radius=radius)
            for x in range(4)
        ])
        circles.set_stroke(WHITE, 2)
        circles.set_fill(BLUE_E, 1)
        circles[0].set_fill(GREY_BROWN)
        circles.arrange_in_grid()
        for circle in circles:
            formula = OldTex("\\pi", "R", "^2")
            formula.set_color_by_tex("R", YELLOW)
            formula.scale(2)
            formula.move_to(circle)
            circle.add(formula)

        equals = OldTex("=")
        equals.scale(3)

        group = VGroup(sphere, equals, circles)
        group.arrange(RIGHT, buff=MED_SMALL_BUFF)
        equals.shift(3 * SMALL_BUFF * RIGHT)

        why = OldTexText("Why?!")
        why.set_color(YELLOW)
        why.scale(2.5)
        why.next_to(sphere, UP)

        sa_formula = OldTex("4\\pi", "R", "^2")
        sa_formula.set_color_by_tex("R", YELLOW)
        sa_formula.scale(2)
        sa_formula.next_to(sphere, DOWN)

        self.camera.distance_tracker.set_value(100)

        self.add(sphere, equals, circles, why, sa_formula)
