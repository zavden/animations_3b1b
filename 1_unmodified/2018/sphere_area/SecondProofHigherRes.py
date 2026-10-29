# ==============================================================================
# Scene:      SecondProofHigherRes
# Source:     videos/_2018/sphere_area.py (lines 3276-3281)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SecondProofHigherRes.py SecondProofHigherRes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SecondProof(SpecialThreeDScene):
    CONFIG = {
        "sphere_config": {
            "resolution": (30, 30),
        },
        "n_random_subsets": 12,
    }

    def construct(self):
        self.setup_shapes()
        self.divide_into_rings()
        self.show_shadows()
        self.correspond_to_every_other_ring()
        self.cut_cross_section()
        self.show_theta()
        self.enumerate_rings()
        self.ask_about_ring_circumference()
        self.ask_about_shadow_area()
        self.ask_about_2_to_1_correspondance()
        self.show_all_shadow_rings()
        self.ask_about_global_correspondance()

    def setup_shapes(self):
        sphere = self.get_sphere()
        sphere.set_stroke(WHITE, width=0.25)
        self.add(sphere)
        self.sphere = sphere

        u_values, v_values = sphere.get_u_values_and_v_values()
        rings = VGroup(*[VGroup() for u in u_values])
        for piece in sphere:
            rings[piece.u_index].add(piece.copy())
        self.set_ring_colors(rings)
        self.rings = rings

        self.axes = self.get_axes()
        self.add(self.axes)

        self.set_camera_to_default_position()
        self.begin_ambient_camera_rotation()

    def divide_into_rings(self):
        rings = self.rings

        self.play(FadeIn(rings), FadeOut(self.sphere))
        self.play(
            rings.space_out_submobjects, 1.5,
            rate_func=there_and_back_with_pause,
            run_time=3
        )
        self.wait(2)
        rings.save_state()

    def show_shadows(self):
        rings = self.rings
        north_rings = rings[:len(rings) // 2]
        ghost_rings = rings.copy()
        ghost_rings.set_fill(opacity=0.0)
        ghost_rings.set_stroke(WHITE, width=0.5, opacity=0.2)

        north_rings.submobjects.reverse()
        shadows = self.get_shadow(north_rings)
        for piece in shadows.family_members_with_points():
            piece.set_stroke(
                piece.get_fill_color(),
                width=0.5,
            )
        for shadow in shadows:
            shadow.save_state()
        shadows.become(north_rings)

        self.add(ghost_rings)
        self.play(FadeOut(rings), Animation(shadows))
        self.play(LaggedStartMap(Restore, shadows))
        self.wait()
        self.move_camera(phi=40 * DEGREES)
        self.wait(3)

        # Show circle
        radius = self.sphere_config["radius"]
        radial_line = Line(ORIGIN, radius * RIGHT)
        radial_line.set_stroke(RED)
        R_label = OldTex("R")
        R_label.set_background_stroke(width=1)
        R_label.next_to(radial_line, DOWN)

        self.play(
            FadeInFromDown(R_label),
            ShowCreation(radial_line)
        )
        self.play(Rotating(
            radial_line, angle=TAU,
            about_point=ORIGIN,
            rate_func=smooth,
            run_time=3,
        ))
        self.wait()

        self.set_variables_as_attrs(
            shadows, ghost_rings,
            radial_line, R_label
        )

    def correspond_to_every_other_ring(self):
        rings = self.rings
        shadows = self.shadows
        shadows.submobjects.reverse()

        rings.restore()
        self.set_ring_colors(rings)
        every_other_ring = rings[1::2]
        self.move_camera(
            phi=70 * DEGREES,
            theta=-135 * DEGREES,
            added_anims=[
                FadeOut(self.R_label),
                FadeOut(self.radial_line),
            ],
            run_time=2,
        )
        shadows_copy = shadows.copy()
        shadows.fade(1)
        self.play(
            ReplacementTransform(
                shadows_copy, every_other_ring
            ),
            FadeOut(self.ghost_rings),
            run_time=2,
        )
        self.wait(5)

        self.every_other_ring = every_other_ring

    def cut_cross_section(self):
        shadows = self.shadows
        every_other_ring = self.every_other_ring
        rings = self.rings

        back_half = self.get_hemisphere(rings, UP)
        front_half = self.get_hemisphere(rings, DOWN)
        front_half_ghost = front_half.copy()
        front_half_ghost.set_fill(opacity=0.2)
        front_half_ghost.set_stroke(opacity=0)

        # shaded_back_half = back_half.copy()
        # for piece in shaded_back_half.family_members_with_points():
        #     piece.set_points(piece.get_points()[::-1])
        # shaded_back_half.scale(0.999)
        # shaded_back_half.set_fill(opacity=0.5)

        radius = self.sphere_config["radius"]
        circle = Circle(radius=radius)
        circle.set_stroke(PINK, 2)
        circle.rotate(90 * DEGREES, RIGHT)

        every_other_ring_copy = every_other_ring.copy()
        self.add(every_other_ring_copy)
        self.remove(every_other_ring)
        rings.set_fill(opacity=0.8)
        rings.set_stroke(opacity=0.6)
        self.play(
            FadeIn(back_half),
            FadeIn(front_half_ghost),
            FadeIn(circle),
            FadeOut(shadows),
            FadeOut(every_other_ring_copy),
        )
        self.wait()

        self.set_variables_as_attrs(
            back_half, front_half,
            front_half_ghost,
            slice_circle=circle
        )

    def show_theta(self):
        theta_tracker = ValueTracker(0)
        get_theta = theta_tracker.get_value
        theta_group = always_redraw(
            lambda: self.get_theta_group(get_theta())
        )
        theta_mob_opacity_tracker = ValueTracker(0)
        get_theta_mob_opacity = theta_mob_opacity_tracker.get_value
        theta_mob = theta_group[-1]
        theta_mob.add_updater(
            lambda m: m.set_fill(opacity=get_theta_mob_opacity())
        )
        theta_mob.add_updater(
            lambda m: m.set_background_stroke(
                width=get_theta_mob_opacity()
            )
        )

        lit_ring = always_redraw(
            lambda: self.get_ring_from_theta(
                self.rings, get_theta()
            ).copy().set_color(YELLOW)
        )

        self.stop_ambient_camera_rotation()
        self.move_camera(theta=-60 * DEGREES)

        self.add(theta_group, lit_ring)
        n_rings = len(self.rings) - 1
        lit_ring_index = int((30 / 180) * n_rings)
        angle = PI * lit_ring_index / n_rings
        for alpha in [angle, 0, PI, angle]:
            self.play(
                theta_tracker.set_value, alpha,
                theta_mob_opacity_tracker.set_value, 1,
                Animation(self.camera.phi_tracker),
                run_time=2,
            )
            self.wait()

        # Label d-theta
        radius = self.sphere_config["radius"]
        d_theta = PI / len(self.rings)
        alt_theta = get_theta() + d_theta
        alt_theta_group = self.get_theta_group(alt_theta)
        alt_R_line = alt_theta_group[1]
        # d_theta_arc = Arc(
        #     start_angle=get_theta(),
        #     angle=d_theta,
        #     radius=theta_group[0].radius,
        #     stroke_color=PINK,
        #     stroke_width=3,
        # )
        # d_theta_arc.rotate(90 * DEGREES, axis=RIGHT, about_point=ORIGIN)
        brace = Brace(Line(ORIGIN, radius * d_theta * RIGHT), UP)
        brace.rotate(90 * DEGREES, RIGHT)
        brace.next_to(self.sphere, OUT, buff=0)
        brace.add_to_back(brace.copy().set_stroke(BLACK, 3))
        brace.rotate(
            get_theta() + d_theta / 2,
            axis=UP,
            about_point=ORIGIN,
        )
        brace_label = OldTex("R\\,d\\theta")
        brace_label.rotate(90 * DEGREES, RIGHT)
        brace_label.next_to(brace, OUT + RIGHT, buff=0)
        radial_line = self.radial_line
        R_label = self.R_label
        R_label.rotate(90 * DEGREES, RIGHT)
        R_label.next_to(radial_line, IN, SMALL_BUFF)

        self.play(
            TransformFromCopy(theta_group[1], alt_R_line),
            GrowFromCenter(brace),
            Animation(self.camera.phi_tracker),
        )
        self.wait()
        self.move_camera(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
        )
        self.wait()
        self.play(
            FadeIn(brace_label, IN),
        )
        self.play(
            ShowCreation(radial_line),
            FadeIn(R_label),
        )
        self.wait()
        self.move_camera(
            phi=70 * DEGREES,
            theta=-70 * DEGREES,
        )
        self.wait(3)

        self.set_variables_as_attrs(
            theta_tracker, lit_ring, theta_group,
            brace, brace_label, d_theta,
            alt_R_line, theta_mob_opacity_tracker,
        )

    def enumerate_rings(self):
        pass  # Skip, for now...

    def ask_about_ring_circumference(self):
        theta = self.theta_tracker.get_value()
        radius = self.sphere_config["radius"]
        circle = Circle(
            radius=radius * np.sin(theta)
        )
        circle.shift(radius * np.cos(theta) * OUT)
        circle.set_stroke(Color("red"), 5)

        to_fade = VGroup(
            self.R_label, self.radial_line,
            self.brace, self.brace_label
        )

        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            added_anims=[FadeOut(to_fade)]
        )
        self.play(ShowCreation(circle))
        self.wait()
        self.move_camera(
            phi=70 * DEGREES,
            theta=-70 * DEGREES,
            added_anims=[
                FadeIn(to_fade),
                FadeOut(circle),
            ]
        )
        self.wait()

    def ask_about_shadow_area(self):
        lit_ring = self.lit_ring
        lit_ring_copy = lit_ring.copy()
        lit_ring_copy.clear_updaters()

        all_shadows = self.shadows
        all_shadows.set_fill(BLUE_E, 0.5)
        for piece in all_shadows.family_members_with_points():
            piece.set_stroke(width=0)

        radius = self.sphere_config["radius"]
        shadow = self.get_shadow(lit_ring)
        theta = self.theta_tracker.get_value()
        d_theta = self.d_theta

        def get_dashed_line(angle):
            p0 = np.cos(angle) * OUT + np.sin(angle) * RIGHT
            p0 *= radius
            p1 = np.array([*p0[:2], 0])
            result = DashedLine(p0, p1)
            result.set_stroke(WHITE, 1)
            result.add_to_back(
                result.copy().set_stroke(BLACK, 2)
            )
            result.set_shade_in_3d(True)
            return result

        dashed_lines = VGroup(*[
            get_dashed_line(t)
            for t in [theta, theta + d_theta]
        ])

        self.play(
            ReplacementTransform(lit_ring_copy, shadow),
            FadeOut(self.R_label),
            FadeOut(self.radial_line),
            Animation(self.camera.phi_tracker),
            *map(ShowCreation, dashed_lines),
            run_time=2,
        )
        self.wait(2)

        self.set_variables_as_attrs(
            dashed_lines,
            lit_shadow=shadow,
        )

    def ask_about_2_to_1_correspondance(self):
        theta_tracker = ValueTracker(0)
        get_theta = theta_tracker.get_value
        new_lit_ring = always_redraw(
            lambda: self.get_ring_from_theta(
                self.rings, get_theta()
            ).copy().set_color(PINK)
        )

        self.add(new_lit_ring)
        for angle in [PI, 0, PI]:
            self.play(
                theta_tracker.set_value, angle,
                Animation(self.camera.phi_tracker),
                run_time=3
            )
        self.remove(new_lit_ring)
        self.remove(theta_tracker)

    def show_all_shadow_rings(self):
        lit_ring_copy = self.lit_ring.copy()
        lit_ring_copy.clear_updaters()
        self.remove(self.lit_ring)
        theta_group_copy = self.theta_group.copy()
        theta_group_copy.clear_updaters()
        self.remove(self.theta_group, *self.theta_group)
        to_fade = VGroup(
            theta_group_copy, self.alt_R_line,
            self.brace, self.brace_label,
            lit_ring_copy, self.lit_shadow,
            self.slice_circle,
            self.dashed_lines,
        )

        R_label = self.R_label
        radial_line = self.radial_line
        R_label.rotate(
            -90 * DEGREES,
            axis=RIGHT, about_point=radial_line.get_center()
        )
        shadows = self.shadows
        self.set_ring_colors(shadows, [GREY_BROWN, GREY_D])
        for submob in shadows:
            submob.save_state()
        shadows.become(self.rings.saved_state[:len(shadows)])

        self.play(
            FadeOut(to_fade),
            LaggedStartMap(FadeIn, shadows),
            self.theta_mob_opacity_tracker.set_value, 0,
        )
        self.play(
            LaggedStartMap(Restore, shadows),
            ApplyMethod(
                self.camera.phi_tracker.set_value, 60 * DEGREES,
            ),
            ApplyMethod(
                self.camera.theta_tracker.set_value, -130 * DEGREES,
            ),
            run_time=3
        )
        self.play(
            ShowCreation(radial_line),
            FadeIn(R_label),
            Animation(self.camera.phi_tracker),
        )
        self.begin_ambient_camera_rotation()
        self.wait()

        rings = self.rings
        rings_copy = rings.saved_state.copy()
        self.set_ring_colors(rings_copy)
        self.play(
            FadeOut(R_label),
            FadeOut(radial_line),
            FadeIn(rings_copy)
        )
        self.remove(rings_copy)
        rings.become(rings_copy)
        self.add(rings)

    def ask_about_global_correspondance(self):
        rings = self.rings

        self.play(
            FadeOut(rings[::2])
        )
        self.wait(8)

    #
    def set_ring_colors(self, rings, colors=[BLUE_E, BLUE_D]):
        for i, ring in enumerate(rings):
            color = colors[i % len(colors)]
            ring.set_fill(color, opacity=1)
            ring.set_stroke(color, width=0.5, opacity=1)
            for piece in ring:
                piece.insert_n_curves(4)
                piece.on_sphere = True
                piece.set_points([
                    *piece.get_points()[3:-1],
                    *piece.get_points()[:3],
                    piece.get_points()[3]
                ])
        return rings

    def get_shadow(self, mobject):
        result = mobject.copy()
        result.apply_function(
            lambda p: np.array([*p[:2], 0])
        )
        return result

    def get_hemisphere(self, group, vect):
        if len(group.submobjects) == 0:
            if np.dot(group.get_center(), vect) > 0:
                return group
            else:
                return VMobject()
        else:
            return VGroup(*[
                self.get_hemisphere(submob, vect)
                for submob in group
            ])

    def get_northern_hemisphere(self, group):
        return self.get_hemisphere(group, OUT)

    def get_theta(self, ring):
        piece = ring[0]
        point = piece.get_points()[3]
        return np.arccos(point[2] / get_norm(point))

    def get_theta_group(self, theta):
        arc = Arc(
            start_angle=90 * DEGREES,
            angle=-theta,
            radius=0.5,
        )
        arc.rotate(90 * DEGREES, RIGHT, about_point=ORIGIN)
        arc.set_stroke(YELLOW, 2)
        theta_mob = OldTex("\\theta")
        theta_mob.rotate(90 * DEGREES, RIGHT)
        vect = np.cos(theta / 2) * OUT + np.sin(theta / 2) * RIGHT
        theta_mob.move_to(
            (arc.radius + 0.25) * normalize(vect),
        )
        theta_mob.set_background_stroke(width=1)

        radius = self.sphere_config["radius"]
        point = arc.point_from_proportion(1)
        radial_line = Line(
            ORIGIN, radius * normalize(point)
        )
        radial_line.set_stroke(WHITE, 2)

        return VGroup(arc, radial_line, theta_mob)

    def get_ring_from_theta(self, rings, theta):
        n_rings = len(rings)
        index = min(int((theta / PI) * n_rings), n_rings - 1)
        return rings[index]


class SecondProofHigherRes(SecondProof):
    CONFIG = {
        "sphere_config": {
            "resolution": (60, 60),
        },
    }
