# ==============================================================================
# Scene:      TwoDScreenInOurThreeDWorld
# Source:     videos/_2018/WindingNumber_G.py (lines 1065-1154)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl TwoDScreenInOurThreeDWorld.py TwoDScreenInOurThreeDWorld -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - should_shade_in_3d() is not defined anywhere (NameError in Cairo too); the Mobject method does what it meant
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/WindingNumber.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7



# ----- From _2018/WindingNumber_G.py -----

class AltTeacherStudentsScene(TeacherStudentsScene):
    def setup(self):
        TeacherStudentsScene.setup(self)
        self.teacher.set_color(YELLOW_E)


class TwoDScreenInOurThreeDWorld(AltTeacherStudentsScene, ThreeDScene):
    def construct(self):
        self.ask_about_2d_functions()
        self.show_3d()

    def ask_about_2d_functions(self):
        in_plane = NumberPlane(x_radius = 2.5, y_radius = 2.5)
        in_plane.add_coordinates()
        in_plane.set_height(3)
        out_plane = in_plane.copy()

        in_text = OldTexText("Input space")
        out_text = OldTexText("Output space")
        VGroup(in_text, out_text).scale(0.75)
        in_text.next_to(in_plane, UP, SMALL_BUFF)
        out_text.next_to(out_plane, UP, SMALL_BUFF)
        in_plane.add(in_text)
        out_plane.add(out_text)

        arrow = Arrow(
            LEFT, RIGHT, 
            path_arc = -TAU/4,
            color = WHITE
        )
        arrow.pointwise_become_partial(arrow, 0.0, 0.97)
        group = VGroup(in_plane, arrow, out_plane)
        group.arrange(RIGHT)
        arrow.shift(UP)
        group.move_to(self.students)
        group.to_edge(UP)

        dots = VGroup()
        dots_target = VGroup()
        for x in np.arange(-2.5, 3.0, 0.5):
            for y in np.arange(-2.5, 3.0, 0.5):
                dot = Dot(radius = 0.05)
                dot.move_to(in_plane.coords_to_point(x, y))
                dot.generate_target()
                dot.target.move_to(out_plane.coords_to_point(
                    x + 0.25*np.cos(5*y), y + 0.25*np.sin(3*x)
                ))
                dots.add(dot)
                dots_target.add(dot.target)
        dots.set_color_by_gradient(YELLOW, RED)
        dots_target.set_color_by_gradient(YELLOW, RED)

        self.play(
            self.teacher.change, "raise_right_hand",
            Write(in_plane, run_time = 1)
        )
        self.play(
            ShowCreation(arrow),
            ReplacementTransform(
                in_plane.copy(), out_plane,
                path_arc = -TAU/4,
            )
        )
        self.play(
            LaggedStartMap(GrowFromCenter, dots, run_time = 1),
            self.change_students(*3*["erm"]),
        )
        self.play(LaggedStartMap(MoveToTarget, dots, path_arc = -TAU/4))
        self.wait(3)


    def show_3d(self):
        laptop = Laptop().scale(2)
        laptop.rotate(-TAU/12, DOWN)
        laptop.rotate(-5*TAU/24, LEFT)
        laptop.rotate(TAU/8, LEFT)
        laptop.scale(2.3*FRAME_X_RADIUS/laptop.screen_plate.get_width())
        laptop.shift(-laptop.screen_plate.get_center() + 0.1*IN)
        # CHANGE: should_shade_in_3d() is not defined anywhere (NameError in Cairo too); the Mobject method does what it meant
        laptop.set_shade_in_3d(True)

        everything = VGroup(laptop, *self.mobjects)
        everything.generate_target()
        # for mob in everything.target.get_family():
        #     if isinstance(mob, PiCreature):
        #         mob.change_mode("confused")
        everything.target.rotate(TAU/12, LEFT)
        everything.target.rotate(TAU/16, UP)
        everything.target.shift(4*UP)

        self.move_camera(
            distance = 12,
            run_time = 4,
            added_anims = [MoveToTarget(everything, run_time = 4)],
        )
        always_rotate(everything, axis=UP, rate=3 * DEGREES)
        self.wait(10)
