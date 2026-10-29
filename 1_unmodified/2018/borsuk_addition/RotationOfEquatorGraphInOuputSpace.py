# ==============================================================================
# Scene:      RotationOfEquatorGraphInOuputSpace
# Source:     videos/_2018/borsuk_addition.py (lines 1035-1055)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl RotationOfEquatorGraphInOuputSpace.py RotationOfEquatorGraphInOuputSpace -w -m --fps 15
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


class FunctionGOutputSpace(FunctionGInputSpace):
    def construct(self):
        self.show_input_dot()
        self.show_start_path()
        self.show_antipodal_point()
        self.show_equator()
        self.deform_towards_north_pole()

    def setup(self):
        axes = self.axes = Axes(
            x_min=-2.5,
            x_max=2.5,
            y_min=-2.5,
            y_max=2.5,
            axis_config={'unit_size': 1.5}
        )
        for axis in axes:
            numbers = list(range(-2, 3))
            numbers.remove(0)
            axis.add_numbers(*numbers)

        self.init_tracked_point()
        self.init_dot()

    def show_input_dot(self):
        axes = self.axes
        dot = self.dot
        point_mob = self.tracked_point

        point_mob.move_to(self.get_start_point())
        self.add(dot)
        self.update_mobjects(0)
        self.remove(dot)

        p_tex = "\\vec{\\textbf{p}}"
        fp_label = self.fp_label = OldTex("f(", p_tex, ")")
        fp_label.set_color_by_tex(p_tex, YELLOW)

        self.play(Write(axes, run_time=3))
        self.wait(3)
        dc = dot.copy()
        self.play(
            FadeIn(dc, 2 * UP, remover=True),
            UpdateFromFunc(fp_label, lambda fp: fp.next_to(dc, UL, SMALL_BUFF))
        )
        self.add(dot)
        fp_label.add_updater(
            lambda fp: fp.next_to(dot, UL, SMALL_BUFF)
        )
        self.wait(2)

    def draw_path(self, path,
                  run_time=4,
                  dot_follow=True,
                  uncreate=False,
                  added_anims=None
                  ):
        added_anims = added_anims or []
        point_mob = self.tracked_point
        shadow_path = path.deepcopy().fade(1)
        flat_path = self.modify_path(path)
        anims = [
            ShowCreation(flat_path),
            ShowCreation(shadow_path),
        ]
        if dot_follow:
            anims.append(UpdateFromFunc(
                point_mob,
                lambda p: p.move_to(shadow_path.point_from_proportion(1))
            ))
        self.add(flat_path, self.dot)
        self.play(*anims, run_time=run_time)

        if uncreate:
            self.wait()
            self.remove(shadow_path)
            self.play(
                Uncreate(flat_path),
                run_time=run_time
            )

    def show_antipodal_point(self):
        dot = self.dot
        pre_path = VMobject().set_points_smoothly([
            ORIGIN, DOWN, DOWN + 2 * RIGHT,
            3 * RIGHT + 0.5 * UP, 0.5 * RIGHT, ORIGIN
        ])
        pre_path.rotate(-45 * DEGREES, about_point=ORIGIN)
        pre_path.shift(dot.get_center())
        path = DashedVMobject(pre_path)

        fp_label = self.fp_label
        equals = OldTex("=")
        equals.next_to(fp_label, RIGHT, SMALL_BUFF)
        f_neg_p = OldTex("f(", "-\\vec{\\textbf{p}}", ")")
        f_neg_p[1].set_color(RED)
        f_neg_p.next_to(equals, RIGHT)

        gp_label = OldTex("g", "(", "\\vec{\\textbf{p}}", ")")
        gp_label[0].set_color(GREEN)
        gp_label[2].set_color(YELLOW)
        gp_label.add_updater(lambda m: m.next_to(dot, UL, SMALL_BUFF))
        self.gp_label = gp_label
        # gp_label.next_to(Dot(ORIGIN), UL, SMALL_BUFF)

        self.play(ShowCreation(path, run_time=4))
        self.wait()
        self.play(
            Write(equals),
            Write(f_neg_p),
        )
        self.wait(6)
        self.play(
            FadeOut(VGroup(path, equals, f_neg_p))
        )
        dot.clear_updaters()
        self.add(fp_label, gp_label)
        gp_label.set_background_stroke(width=0)
        self.play(
            dot.move_to, ORIGIN,
            VFadeOut(fp_label),
            VFadeIn(gp_label),
        )
        self.wait(4)
        self.play(
            dot.move_to, self.odd_func(self.get_start_point())
        )
        # Flip, 2 second for flip, 7 seconds after
        path = self.get_antipodal_path()
        path.apply_function(self.odd_func)
        end_dot = Dot(color=RED)
        end_dot.move_to(path[-1].point_from_proportion(1))
        g_neg_p = OldTex(
            "g", "(", "-\\vec{\\textbf{p}}", ")"
        )
        g_neg_p[0].set_color(GREEN)
        g_neg_p[2].set_color(RED)
        g_neg_p.next_to(end_dot, UR, SMALL_BUFF)
        reflection_line = DashedLine(
            dot.get_center(), end_dot.get_center(),
            stroke_width=0,
        )
        vector = Vector(dot.get_center())

        self.play(ShowCreation(path, run_time=1))
        self.wait()
        self.play(
            ShowCreationThenDestruction(reflection_line, run_time=2),
            TransformFromCopy(dot, end_dot),
            ReplacementTransform(
                gp_label.deepcopy().clear_updaters(), g_neg_p
            ),
        )
        self.wait()
        self.play(FadeIn(vector))
        self.play(Rotate(vector, angle=PI, about_point=ORIGIN))
        self.play(FadeOut(vector))
        self.play(
            FadeOut(end_dot),
            FadeOut(g_neg_p),
            FadeOut(path),
        )

    def show_equator(self):
        dot = self.dot
        point_mob = self.tracked_point
        equator = self.get_lat_line()
        flat_eq = equator.deepcopy().apply_function(self.odd_func)
        equator.fade(1)

        equator_start = equator[0].point_from_proportion(0)

        # To address
        self.play(
            point_mob.move_to, equator_start,
            dot.move_to, self.odd_func(equator_start)
        )
        dot.add_updater(lambda m: m.move_to(
            self.odd_func(point_mob.get_center())
        ))
        self.play(
            ShowCreation(equator),
            ShowCreation(flat_eq),
            run_time=4,
        )
        for x in range(2):
            self.play(
                Rotate(point_mob, PI, about_point=ORIGIN, axis=OUT),
                run_time=4
            )
            self.wait(3)
        self.play(
            FadeOut(self.dot),
            FadeOut(self.gp_label),
        )

        self.equator = equator
        self.flat_eq = flat_eq

    def deform_towards_north_pole(self):
        equator = self.equator
        flat_eq = self.flat_eq

        self.play(
            UpdateFromAlphaFunc(
                equator,
                lambda m, a: m.become(self.get_lat_line(a * PI / 2)).set_stroke(width=0),
                run_time=16
            ),
            UpdateFromFunc(
                flat_eq,
                lambda m: m.become(
                    equator.deepcopy().apply_function(self.odd_func).set_stroke(
                        color=RED, width=3
                    )
                )
            )
        )
        self.wait()
    #

    def func(self, point):
        x, y, z = point
        return 0.5 * self.axes.coords_to_point(
            2 * x + 0.5 * y + z,
            2 * y - 0.5 * np.sin(PI * x) + z**2 + 1 - x,
        )

    def odd_func(self, point):
        return (self.func(point) - self.func(-point)) / 2

    def get_dot(self, point):
        return Dot(self.func(point))

    def modify_path(self, path):
        path.apply_function(self.func)
        return path


class RotationOfEquatorGraphInOuputSpace(FunctionGOutputSpace):
    def construct(self):
        self.add(self.axes)
        equator = self.get_lat_line(0)
        equator.remove(*equator[len(equator) // 2:])

        flat_eq = equator.copy().apply_function(self.odd_func)
        vector = Vector(flat_eq[0].point_from_proportion(0))
        vector_copy = vector.copy().fade(0.5)

        self.add(flat_eq)
        self.add(flat_eq.copy())
        self.wait()
        self.play(FadeIn(vector))
        self.add(vector_copy)
        self.play(
            Rotate(
                VGroup(flat_eq, vector),
                PI, about_point=ORIGIN, run_time=5
        ))
        self.play(FadeOut(vector), FadeOut(vector_copy))
