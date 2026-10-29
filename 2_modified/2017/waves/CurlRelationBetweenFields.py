# ==============================================================================
# Scene:      CurlRelationBetweenFields
# Source:     videos/_2017/waves.py (lines 860-951)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CurlRelationBetweenFields.py CurlRelationBetweenFields -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - old rotate(angle, axis, axes, point) signature: pass the centre as about_point
#   - old rotate(angle, axis, axes, point) signature: pass the centre as about_point
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


E_COLOR = BLUE


M_COLOR = YELLOW


class CurlRelationBetweenFields(ThreeDScene):
    def construct(self):
        self.add_axes()
        self.loop_in_E()
        self.loop_in_M()
        self.second_loop_in_E()

    def add_axes(self):
        self.add(ThreeDAxes(x_axis_radius = FRAME_X_RADIUS))

    def loop_in_E(self):
        E_vects = VGroup(*[
            Vector(0.5*rotate_vector(vect, np.pi/2)).shift(vect)
            for vect in compass_directions(8)
        ])
        E_vects.set_color(E_COLOR)
        point = 1.2*RIGHT + 2*UP + OUT
        E_vects.shift(point)

        M_vect = Vector(
            IN, 
            normal_vector = DOWN,
            color = M_COLOR
        )
        M_vect.shift(point)
        M_vect.save_state()
        M_vect.scale(0.01, about_point = M_vect.get_start())

        self.play(ShowCreation(E_vects, run_time = 2))
        self.wait()
        self.move_camera(0.8*np.pi/2, -0.45*np.pi)
        self.begin_ambient_camera_rotation()
        self.play(M_vect.restore, run_time = 3, rate_func=linear)
        self.wait(3)

        self.E_vects = E_vects
        self.E_circle_center = point
        self.M_vect = M_vect

    def loop_in_M(self):
        M_vects = VGroup(*[
            Vector(
                rotate_vector(vect, np.pi/2),
                normal_vector = IN,
                color = M_COLOR
            ).shift(vect)
            for vect in compass_directions(8, LEFT)[1:]
        ])
        M_vects.rotate(np.pi/2, RIGHT)
        new_point = self.E_circle_center + RIGHT
        M_vects.shift(new_point)

        E_vect = self.E_vects[0]

        self.play(
            ShowCreation(M_vects, run_time = 2),
            *list(map(FadeOut, self.E_vects[1:]))
        )
        self.wait()
        self.play(
            # CHANGE: old rotate(angle, axis, axes, point) signature: pass the centre as about_point
            E_vect.rotate, np.pi, RIGHT, {"about_point": new_point},
            E_vect.scale_about_point, 3, new_point,
            run_time = 4,
            rate_func=linear,
        )
        self.wait()

        self.M_circle_center = new_point
        M_vects.add(self.M_vect)
        self.M_vects = M_vects
        self.E_vect = E_vect

    def second_loop_in_E(self):
        E_vects = VGroup(*[
            Vector(1.5*rotate_vector(vect, np.pi/2)).shift(vect)
            for vect in compass_directions(8, LEFT)[1:]
        ])
        E_vects.set_color(E_COLOR)
        point = self.M_circle_center + RIGHT
        E_vects.shift(point)

        M_vect = self.M_vects[3]
        self.M_vects.remove(M_vect)

        self.play(FadeOut(self.M_vects))
        self.play(ShowCreation(E_vects), Animation(M_vect))
        self.play(
            # CHANGE: old rotate(angle, axis, axes, point) signature: pass the centre as about_point
            M_vect.rotate, np.pi, RIGHT, {"about_point": point},
            run_time = 5,
            rate_func=linear,
        )
        self.wait(3)
