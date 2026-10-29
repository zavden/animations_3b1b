# ==============================================================================
# Scene:      DiameterTheorem
# Source:     videos/_2018/basel/basel2.py (lines 2748-2808)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DiameterTheorem.py DiameterTheorem -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo indexing of a mobject with points counted itself first (split() = [self] + submobjects); the copied point is submobjects[0]
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class DiameterTheorem(TeacherStudentsScene):
    def construct(self):
        circle = Circle(radius = 2, color = WHITE)
        circle.next_to(self.students[2], UP)
        self.add(circle)

        center = Dot(circle.get_center(), color = WHITE)
        self.add_foreground_mobject(center)

        diameter_word = OldTexText("Diameter")
        diameter_word.next_to(center, DOWN, SMALL_BUFF)

        point = VectorizedPoint(circle.get_top())
        triangle = Polygon(LEFT, RIGHT, UP)
        triangle.set_stroke(BLUE)
        triangle.set_fill(WHITE, 0.5)
        def update_triangle(triangle):
            triangle.set_points_as_corners([
                circle.get_left(), circle.get_right(),
                point.get_center(), circle.get_left(),
            ])
        triangle_update_anim = Mobject.add_updater(
            triangle, update_triangle
        )
        triangle_update_anim.update(0)

        perp_mark = VMobject()
        perp_mark.set_points_as_corners([LEFT, DOWN, RIGHT])
        perp_mark.shift(DOWN)
        perp_mark.scale(0.15, about_point = ORIGIN)
        perp_mark.shift(point.get_center())
        perp_mark.add(point.copy())

        self.play(
            self.teacher.change, "raise_right_hand",
            DrawBorderThenFill(triangle),
            Write(diameter_word),
        )
        self.play(
            ShowCreation(perp_mark),
            self.change_students(*["pondering"]*3)
        )
        self.add_foreground_mobjects(perp_mark)
        self.add(triangle_update_anim)
        for angle in 0.2*TAU, -0.4*TAU, 0.3*TAU:
            point.generate_target()
            point.target.rotate(angle, about_point = circle.get_center())

            perp_mark.generate_target()
            perp_mark.target.rotate(angle/2)
            perp_mark.target.shift(
                point.target.get_center() - \
                # CHANGE: Cairo indexing of a mobject with points counted itself first (split() = [self] + submobjects); the copied point is submobjects[0]
                perp_mark.target.submobjects[0].get_center()
            )

            self.play(
                MoveToTarget(point),
                MoveToTarget(perp_mark),
                path_arc = angle,
                run_time = 3,
            )
