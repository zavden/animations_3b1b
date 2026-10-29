# ==============================================================================
# Scene:      FunctionGInputSpace
# Source:     videos/_2018/borsuk_addition.py (lines 549-793)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl FunctionGInputSpace.py FunctionGInputSpace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class FunctionGInputSpace(SpecialThreeDScene):
    def setup(self):
        self.init_tracked_point()

        sphere = self.get_sphere()
        sphere.set_fill(BLUE_E, opacity=0.5)
        self.sphere = sphere

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-120 * DEGREES,
        )
        self.begin_ambient_camera_rotation(rate=0.02)

        self.init_dot()

        self.add(ThreeDAxes())

    def construct(self):
        self.show_input_dot()
        self.show_start_path()
        self.show_antipodal_point()
        self.show_equator()
        self.deform_towards_north_pole()

    def show_input_dot(self):
        sphere = self.sphere
        dot = self.dot
        point_mob = self.tracked_point
        start_point = self.get_start_point()

        arrow = Arrow(
            start_point + (LEFT + OUT + UP), start_point,
            color=BLUE,
            buff=MED_LARGE_BUFF,
        )
        arrow.rotate(90 * DEGREES, axis=arrow.get_vector())
        arrow.add_to_back(arrow.copy().set_stroke(BLACK, 5))

        p_label = self.p_label = OldTex("\\vec{\\textbf{p}}")
        p_label.set_color(YELLOW)
        p_label.next_to(arrow.get_start(), OUT, buff=0.3)
        p_label.set_shade_in_3d(True)

        self.play(Write(sphere, run_time=3))
        self.add(dot)
        self.add_fixed_orientation_mobjects(p_label)
        self.play(
            point_mob.move_to, start_point,
            GrowArrow(arrow),
            FadeIn(p_label, IN)
        )
        self.wait()
        self.play(
            arrow.scale, 0, {"about_point": arrow.get_end()},
            p_label.next_to, dot, OUT + LEFT, SMALL_BUFF
        )
        p_label.add_updater(lambda p: p.next_to(dot, OUT + LEFT, SMALL_BUFF))
        self.wait(4)

    def show_start_path(self):
        path = self.get_start_path()
        self.draw_path(path, uncreate=True)
        self.wait()

    def show_antipodal_point(self):
        path = self.get_antipodal_path()
        end_dot = always_redraw(
            lambda: self.get_dot(
                path[-1].point_from_proportion(1)
            ).set_color(RED)
        )

        neg_p = OldTex("-\\vec{\\textbf{p}}")
        neg_p.add_updater(
            lambda p: p.next_to(end_dot, UP + RIGHT + IN)
        )
        neg_p.set_color(RED)
        neg_p.set_shade_in_3d(True)

        self.move_camera(
            phi=100 * DEGREES,
            theta=30 * DEGREES,
            added_anims=[ShowCreation(path)],
            run_time=4,
        )
        self.wait()
        self.add_fixed_orientation_mobjects(neg_p)
        self.play(
            FadeInFromLarge(end_dot),
            Write(neg_p)
        )
        self.wait(4)
        self.move_camera(
            phi=70 * DEGREES,
            theta=-120 * DEGREES,
            run_time=2
        )
        self.wait(7)
        # Flip
        self.move_camera(
            phi=100 * DEGREES,
            theta=30 * DEGREES,
            run_time=2,
        )
        self.wait(7)
        self.move_camera(
            phi=70 * DEGREES,
            theta=-120 * DEGREES,
            added_anims=[
                FadeOut(end_dot),
                FadeOut(neg_p),
                FadeOut(path),
            ],
            run_time=2,
        )

    def show_equator(self):
        point_mob = self.tracked_point
        equator = self.get_lat_line()

        self.play(point_mob.move_to, equator[0].point_from_proportion(0))
        self.play(ShowCreation(equator, run_time=4))
        for x in range(2):
            self.play(
                Rotate(point_mob, PI, about_point=ORIGIN, axis=OUT),
                run_time=4
            )
            self.wait(3)
        self.play(
            FadeOut(self.dot),
            FadeOut(self.p_label),
        )

        self.equator = equator

    def deform_towards_north_pole(self):
        equator = self.equator

        self.play(UpdateFromAlphaFunc(
            equator,
            lambda m, a: m.become(self.get_lat_line(a * PI / 2)),
            run_time=16
        ))
        self.wait()

    #
    def init_tracked_point(self):
        self.tracked_point = VectorizedPoint([0, 0, 2])
        self.tracked_point.add_updater(
            lambda p: p.move_to(2 * normalize(p.get_center()))
        )
        self.add(self.tracked_point)

    def init_dot(self):
        self.dot = always_redraw(
            lambda: self.get_dot(self.tracked_point.get_center())
        )

    def get_start_path(self):
        path = ParametricCurve(
            lambda t: np.array([
                -np.sin(TAU * t + TAU / 4),
                np.cos(2 * TAU * t + TAU / 4),
                0
            ]),
            color=RED
        )
        path.scale(0.5)
        path.shift(0.5 * OUT)
        path.rotate(60 * DEGREES, RIGHT, about_point=ORIGIN)
        path.shift(
            self.get_start_point() - path.point_from_proportion(0)
        )
        path.apply_function(lambda p: 2 * normalize(p))
        return path

    def get_antipodal_path(self):
        start = self.get_start_point()
        path = ParametricCurve(
            lambda t: 2.03 * np.array([
                0,
                np.sin(PI * t),
                np.cos(PI * t),
            ]),
            color=YELLOW
        )
        path.apply_matrix(z_to_vector(start))

        dashed_path = DashedVMobject(path)
        dashed_path.set_shade_in_3d(True)

        return dashed_path

    def get_lat_line(self, lat=0):
        equator = ParametricCurve(lambda t: 2.03 * np.array([
            np.cos(lat) * np.sin(TAU * t),
            np.cos(lat) * (-np.cos(TAU * t)),
            np.sin(lat)
        ]))
        equator.rotate(-90 * DEGREES)
        dashed_equator = DashedVMobject(
            equator,
            num_dashes=40,
            color=RED,
        )
        dashed_equator.set_shade_in_3d(True)
        return dashed_equator

    def draw_path(self, path,
                  run_time=4,
                  dot_follow=True,
                  uncreate=False,
                  added_anims=None
                  ):
        added_anims = added_anims or []
        point_mob = self.tracked_point
        anims = [ShowCreation(path)]
        if dot_follow:
            anims.append(UpdateFromFunc(
                point_mob,
                lambda p: p.move_to(path.point_from_proportion(1))
            ))
        self.add(path, self.dot)
        self.play(*anims, run_time=run_time)

        if uncreate:
            self.wait()
            self.play(
                Uncreate(path),
                run_time=run_time
            )

    def modify_path(self, path):
        return path

    def get_start_point(self):
        return 2 * normalize([-1, -1, 1])

    def get_dot(self, point):
        dot = Dot(color=WHITE)
        dot.shift(2.05 * OUT)
        dot.apply_matrix(z_to_vector(normalize(point)))
        dot.set_shade_in_3d(True)
        return dot
