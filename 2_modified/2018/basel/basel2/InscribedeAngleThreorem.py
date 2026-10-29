# ==============================================================================
# Scene:      InscribedeAngleThreorem
# Source:     videos/_2018/basel/basel2.py (lines 2810-2891)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl InscribedeAngleThreorem.py InscribedeAngleThreorem -w -m --fps 15
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


class InscribedeAngleThreorem(TeacherStudentsScene):
    def construct(self):
        circle = Circle(radius = 2, color = WHITE)
        circle.next_to(self.students[2], UP)
        self.add(circle)

        title = OldTexText("Inscribed angle \\\\ theorem")
        title.to_corner(UP+LEFT)
        self.add(title)

        center = Dot(circle.get_center(), color = WHITE)
        self.add_foreground_mobject(center)

        point = VectorizedPoint(circle.get_left())
        shape = Polygon(UP+LEFT, ORIGIN, DOWN+LEFT, RIGHT)
        shape.set_stroke(BLUE)
        def update_shape(shape):
            shape.set_points_as_corners([
                point.get_center(),
                circle.point_from_proportion(7./8), 
                circle.get_center(),
                circle.point_from_proportion(1./8), 
                point.get_center(),
            ])
        shape_update_anim = Mobject.add_updater(
            shape, update_shape
        )
        shape_update_anim.update(0)

        angle_mark = Arc(start_angle = -TAU/8, angle = TAU/4)
        angle_mark.scale(0.3, about_point = ORIGIN)
        angle_mark.shift(circle.get_center())
        theta = OldTex("\\theta").set_color(RED)
        theta.next_to(angle_mark, RIGHT, MED_SMALL_BUFF)
        angle_mark.match_color(theta)

        half_angle_mark = Arc(start_angle = -TAU/16, angle = TAU/8)
        half_angle_mark.scale(0.3, about_point = ORIGIN)
        half_angle_mark.shift(point.get_center())
        half_angle_mark.add(point.copy())
        theta_halves = OldTex("\\theta/2").set_color(GREEN)
        theta_halves.scale(0.7)
        half_angle_mark.match_color(theta_halves)
        theta_halves_update = UpdateFromFunc(
            theta_halves, lambda m : m.move_to(interpolate(
                point.get_center(), 
                half_angle_mark.point_from_proportion(0.5),
                2.5,
            ))
        )
        theta_halves_update.update(0)

        self.play(
            self.teacher.change, "raise_right_hand",
            ShowCreation(shape, rate_func=linear),
        )
        self.play(*list(map(FadeIn, [angle_mark, theta])))
        self.play(
            ShowCreation(half_angle_mark),
            Write(theta_halves),
            self.change_students(*["pondering"]*3)
        )
        self.add_foreground_mobjects(half_angle_mark, theta_halves)
        self.add(shape_update_anim)
        for angle in 0.25*TAU, -0.4*TAU, 0.3*TAU, -0.35*TAU:
            point.generate_target()
            point.target.rotate(angle, about_point = circle.get_center())

            half_angle_mark.generate_target()
            half_angle_mark.target.rotate(angle/2)
            half_angle_mark.target.shift(
                point.target.get_center() - \
                # CHANGE: Cairo indexing of a mobject with points counted itself first (split() = [self] + submobjects); the copied point is submobjects[0]
                half_angle_mark.target.submobjects[0].get_center()
            )

            self.play(
                MoveToTarget(point),
                MoveToTarget(half_angle_mark),
                theta_halves_update,
                path_arc = angle,
                run_time = 3,
            )
