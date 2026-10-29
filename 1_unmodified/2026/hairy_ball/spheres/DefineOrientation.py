# ==============================================================================
# Scene:      DefineOrientation
# Source:     videos/_2026/hairy_ball/spheres.py (lines 1398-1752)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineOrientation.py DefineOrientation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import numpy as np

def get_sphereical_vector_field(
    v_func,
    axes,
    points,
    color=BLUE,
    stroke_width=1,
    mvltss=1.0,
    tip_width_ratio=4,
    tip_len_to_width=0.01,
):

    field = VectorField(
        v_func, axes,
        sample_coords=1.01 * points,
        max_vect_len_to_step_size=mvltss,
        density=1,
        stroke_width=stroke_width,
        tip_width_ratio=tip_width_ratio,
        tip_len_to_width=tip_len_to_width,
    )
    field.apply_depth_test()
    field.set_stroke(color, opacity=0.8)
    field.set_scale_stroke_with_zoom(True)
    return field


class InsideOut(InteractiveScene):
    def construct(self):
        # Show sphere
        frame = self.frame
        self.camera.light_source.move_to([-3, 3, 3])
        radius = 3
        inner_scale = 0.999
        axes = ThreeDAxes((-5, 5), (-5, 5), (-5, 5))
        axes.set_stroke(WHITE, 1, 0.5)
        axes.apply_depth_test()
        axes.z_axis.rotate(0.1 * DEG, RIGHT)

        sphere = self.get_colored_sphere(radius, inner_scale)
        sphere.set_clip_plane(UP, radius)

        mesh = SurfaceMesh(sphere[0], resolution=(61, 31))
        mesh.set_stroke(WHITE, 1, 0.25)

        frame.reorient(-68, 70, 0)
        self.add(axes, sphere, mesh)
        self.play(sphere.animate.set_clip_plane(UP, 0), run_time=2)

        # Show point go to antipoode
        point = radius * normalize(LEFT + OUT)
        p_dot = TrueDot(point, color=YELLOW, radius=0.05).make_3d()
        p_label = Tex(R"p")
        p_label.rotate(90 * DEG, RIGHT).rotate(90 * DEG, IN)
        p_label.next_to(p_dot, OUT, SMALL_BUFF)

        neg_p_dot = p_dot.copy().move_to(-point)
        neg_p_label = Tex(R"-p")
        neg_p_label.rotate(90 * DEG, RIGHT)
        neg_p_label.next_to(neg_p_dot, IN, SMALL_BUFF)

        neg_p_dot.move_to(p_dot)

        dashed_line = DashedLine(point, -point, buff=0)
        dashed_line.set_stroke(YELLOW, 2)

        semi_circle = Arc(135 * DEG, 180 * DEG, radius=radius)
        semi_circle.set_stroke(YELLOW, 3)
        semi_circle.rotate(90 * DEG, RIGHT, about_point=ORIGIN)
        dashed_semi_circle = DashedVMobject(semi_circle, num_dashes=len(dashed_line))

        self.play(
            FadeIn(p_dot, scale=0.5),
            Write(p_label),
        )
        self.play(
            ShowCreation(dashed_semi_circle),
            MoveAlongPath(neg_p_dot, semi_circle, rate_func=linear),
            TransformFromCopy(p_label, neg_p_label, time_span=(2, 3)),
            Rotate(p_label, 90 * DEG, OUT),
            frame.animate.reorient(59, 87, 0),
            run_time=3,
        )
        frame.add_ambient_rotation(-2 * DEG)
        self.wait(2)
        self.play(ReplacementTransform(dashed_semi_circle, dashed_line))
        self.wait(3)

        # Show more antipodes
        angles = np.linspace(0, 90 * DEG, 15)[1:]
        top_dots, low_dots, lines = groups = [
            Group(
                template.copy().rotate(angle, axis=UP, about_point=ORIGIN)
                for angle in angles
            )
            for template in [p_dot, neg_p_dot, dashed_line]
        ]
        for group in groups:
            group.set_submobject_colors_by_gradient(YELLOW, BLUE, interp_by_hsl=True)

        self.play(FadeIn(top_dots, lag_ratio=0.1))
        frame.clear_updaters()
        self.play(
            LaggedStartMap(ShowCreation, lines, lag_ratio=0.25),
            LaggedStart(
                (TransformFromCopy(top_dot, low_dot, rate_func=linear)
                for top_dot, low_dot in zip(top_dots, low_dots)),
                lag_ratio=0.25,
                group_type=Group,
            ),
            frame.animate.reorient(-49, 60, 0),
            run_time=7
        )

        # Just show the cap
        cap = self.get_colored_sphere(radius, inner_scale, v_range=(0.75 * PI, PI))
        frame.clear_updaters()

        self.add(cap, sphere, mesh)
        self.play(
            FadeOut(p_label),
            FadeOut(neg_p_label),
            FadeOut(top_dots),
            FadeOut(lines),
            FadeOut(low_dots),
            FadeOut(p_dot),
            FadeOut(neg_p_dot),
            FadeOut(dashed_line),
            FadeOut(sphere, 0.1 * UP),
            FadeIn(cap),
        )
        self.wait()
        self.play(frame.animate.reorient(-48, 93, 0), run_time=3)
        self.wait()

        # Add normal vectors
        uv_samples = np.array([
            [(u + v) % TAU, v]
            for v in np.linspace(0.75 * PI, 0.95 * PI, 10)
            for u in np.linspace(0, TAU, 20)
        ])
        normal_vectors = VGroup(
            VMobject().set_points_as_corners([ORIGIN, RIGHT, RIGHT, 2 * RIGHT])
            for sample in uv_samples
        )
        for vect in normal_vectors:
            vect.set_stroke(BLUE_B, width=[1, 1, 1, 6, 3, 0], opacity=0.5)
        normal_vectors.apply_depth_test()

        def update_normal_vectors(normal_vectors):
            points = np.array([cap[0].uv_to_point(u, v) for u, v in uv_samples])
            du_points = np.array([cap[0].uv_to_point(u + 0.1, v) for u, v in uv_samples])
            dv_points = np.array([cap[0].uv_to_point(u, v + 0.1) for u, v in uv_samples])
            normals = normalize_along_axis(np.cross(du_points - points, dv_points - points), 1)
            for point, normal, vector in zip(points, normals, normal_vectors):
                vector.put_start_and_end_on(point, point + 0.3 * normal)

        update_normal_vectors(normal_vectors)
        self.play(FadeIn(normal_vectors))

        # Show transition to antipode
        anti_cap = cap.copy().rotate(PI, axis=OUT, about_point=ORIGIN).stretch(-1, 2, about_point=ORIGIN)
        anti_cap[0].shift(1e-2 * OUT)
        all_points = cap[0].get_points()
        indices = random.sample(list(range(len(all_points))), 200)
        pre_points = all_points[indices]
        post_points = -1 * pre_points

        antipode_lines = VGroup(
            Line(point, -point)
            for point in pre_points
        )
        antipode_lines.set_stroke(YELLOW, 1, 0.25)
        antipode_lines.apply_depth_test()

        def update_lines(lines):
            points1 = cap[0].get_points()[indices]
            points2 = anti_cap[0].get_points()[indices]
            for line, p1, p2 in zip(lines, points1, points2):
                line.put_start_and_end_on(p1, p2)

        antipode_lines.add_updater(update_lines)

        rot_arcs = VGroup(
            Arrow(4 * RIGHT, 4 * LEFT, path_arc=180 * DEG, thickness=5),
            Arrow(4 * LEFT, 4 * RIGHT, path_arc=180 * DEG, thickness=5),
        )
        flip_arrows = VGroup(
            Arrow(3 * IN, 3.2 * OUT, thickness=5),
            Arrow(3 * OUT, 3.2 * IN, thickness=5),
        ).rotate(90 * DEG).shift(4 * RIGHT)

        self.play(
            ShowCreation(antipode_lines, lag_ratio=0, suspend_mobject_updating=True),
            frame.animate.reorient(8, 79, 0, (0.0, 0.02, 0.0)),
            run_time=4,
        )
        self.wait()
        normal_vectors.add_updater(update_normal_vectors)
        self.play(
            Write(rot_arcs, lag_ratio=0, run_time=1),
            Rotate(cap, PI, axis=OUT, run_time=3, about_point=ORIGIN),
            Rotate(mesh, PI, axis=OUT, run_time=3, about_point=ORIGIN),
        )
        self.play(FadeOut(rot_arcs))
        self.play(
            FadeIn(flip_arrows, time_span=(0, 1)),
            Transform(cap, anti_cap),
            mesh.animate.stretch(-1, 2, about_point=ORIGIN),
            VFadeOut(antipode_lines),
            run_time=3
        )
        self.play(FadeOut(flip_arrows))
        self.play(frame.animate.reorient(-9, 96, 0, (0.0, 0.02, 0.0)), run_time=5)
        self.wait()

        # Antipode homotopy

    def get_colored_sphere(
        self,
        radius=3,
        inner_scale=0.999,
        outer_color=BLUE_E,
        inner_color=GREY_BROWN,
        u_range=(0, TAU),
        v_range=(0, PI),
    ):
        outer_sphere = Sphere(radius=radius, u_range=u_range, v_range=v_range)
        inner_sphere = outer_sphere.copy()
        outer_sphere.set_color(outer_color, 1)
        inner_sphere.set_color(inner_color, 1)
        inner_sphere.scale(inner_scale)
        return Group(outer_sphere, inner_sphere)

    def old_homotopy(self):
        def homotopy(x, y, z, t, scale=-1):
            p = np.array([x, y, z])
            power = 1 + 0.2 * (x / radius)
            return interpolate(p, scale * p, t**power)

        antipode_lines = VGroup(
            Line(point, -point)
            for point in random.sample(list(cap[0].get_points()), 100)
        )
        antipode_lines.set_stroke(YELLOW, 1, 0.25)

        self.play(
            Homotopy(lambda x, y, z, t: homotopy(x, y, z, t, -inner_scale), cap[0]),
            Homotopy(lambda x, y, z, t: homotopy(x, y, z, t, -1.0 / inner_scale), cap[1]),
            ShowCreation(antipode_lines, lag_ratio=0),
            frame.animate.reorient(-65, 68, 0),
            run_time=3
        )
        self.play(FadeOut(antipode_lines))
        self.play(frame.animate.reorient(-48, 148, 0), run_time=3)
        self.wait()
        self.play(frame.animate.reorient(-70, 83, 0), run_time=3)
        self.play(frame.animate.reorient(-124, 77, 0), run_time=10)


class DefineOrientation(InsideOut):
    def construct(self):
        # Latitude and Longitude
        frame = self.frame
        radius = 3
        sphere = Sphere(radius=radius)
        sphere.set_color(GREY_E, 1)
        earth = TexturedSurface(sphere, "EarthTextureMap", "NightEarthTextureMap")
        earth.set_opacity(0.5)
        mesh = SurfaceMesh(sphere, resolution=(73, 37))
        mesh.set_stroke(WHITE, 1, 0.25)

        uv_tracker = ValueTracker(np.array([180 * DEG, 90 * DEG]))

        dot = TrueDot()
        dot.set_color(YELLOW)
        dot.add_updater(lambda m: m.move_to(sphere.uv_func(*uv_tracker.get_value())))
        dot.set_z_index(2)

        lat_label, lon_label = lat_lon_labels = VGroup(
            Tex(R"\text{Lat: }\, 10^\circ"),
            Tex(R"\text{Lon: }\, 10^\circ"),
        )
        lat_lon_labels.arrange(DOWN, aligned_edge=LEFT)
        lat_lon_labels.fix_in_frame()
        lat_lon_labels.to_corner(UL)
        lat_label.make_number_changeable("10", edge_to_fix=RIGHT).add_updater(
            lambda m: m.set_value(np.round(self.get_lat_lon(*uv_tracker.get_value())[0]))
        )
        lon_label.make_number_changeable("10", edge_to_fix=RIGHT).add_updater(
            lambda m: m.set_value(np.round(self.get_lat_lon(*uv_tracker.get_value())[1]))
        )
        lat_lon_labels.add_updater(lambda m: m.fix_in_frame())

        self.add(sphere, mesh)
        self.add(lat_lon_labels)
        frame.reorient(-66, 85, 0, (-0.06, 0.18, 0.06), 6.78)
        self.play(FadeIn(dot))

        lon_line = TracedPath(dot.get_center, stroke_color=RED)
        self.add(lon_line, dot)
        self.play(uv_tracker.animate.increment_value([0, 30 * DEG]), run_time=4)
        lon_line.suspend_updating()

        lat_line = TracedPath(dot.get_center, stroke_color=TEAL)
        self.add(lat_line, dot)
        self.play(uv_tracker.animate.increment_value([45 * DEG, 0]), run_time=4)
        lat_line.suspend_updating()

        # Add labels to all the points
        u, v = uv_tracker.get_value()

        label_template = Tex(R"(10^\circ, 10^\circ)", isolate=["10"])
        label_template.set_backstroke(BLACK, 1)
        lon_num_template, lat_num_template = label_template.make_number_changeable("10", replace_all=True)

        def get_lat_lon_label(u, v, font_size=5):
            lat, lon = self.get_lat_lon(u, v)
            lat_num_template.set_value(np.round(lat))
            lon_num_template.set_value(np.round(lon))
            label = label_template.copy()
            label.scale(font_size / 48)
            label.move_to(sphere.get_zenith())
            label.rotate(PI - v, axis=RIGHT, about_point=ORIGIN)
            label.rotate(-270 * DEG + u, axis=OUT, about_point=ORIGIN)
            return label

        u_radius = 50 * DEG
        v_radius = 30 * DEG
        all_labels = VGroup(
            get_lat_lon_label(sub_u, sub_v)
            for sub_u in np.arange(u - u_radius, u + u_radius, 10 * DEG)
            for sub_v in np.arange(v - v_radius, v + v_radius, 5 * DEG)
        )
        all_labels.sort(lambda p: get_norm(p - dot.get_center()))

        self.play(
            frame.animate.reorient(-39, 60, 0, (-0.64, 0.45, 0.06), 4.33),
            run_time=3
        )
        self.play(
            FadeIn(all_labels, lag_ratio=0.001, run_time=3),
            dot.animate.set_opacity(0.25),
        )
        self.wait()

        # Show some kind of warping
        def homotopy(x, y, z, t):
            alpha = clip((x + 3) / 6 - 1 + 2 * t, 0, 1)
            shift = wiggle(alpha, 3)
            return (x, y, z + 0.35 * shift)

        dot.suspend_updating()
        group = Group(sphere, mesh, lat_line, lon_line, dot, all_labels)

        self.play(
            Homotopy(homotopy, group, run_time=10)
        )
        dot.resume_updating()
        self.wait()

        # Show tangent vectors
        u, v = uv_tracker.get_value()
        epsilon = 1e-4
        point = sphere.uv_func(u, v)
        u_step = normalize(sphere.uv_func(u + epsilon, v) - point)
        v_step = normalize(sphere.uv_func(u, v + epsilon) - point)

        u_vect = Arrow(point, point + 0.5 * u_step, buff=0, thickness=2).set_color(TEAL)
        v_vect = Arrow(point, point + 0.5 * v_step, buff=0, thickness=2).set_color(RED)
        tangent_vects = VGroup(u_vect, v_vect)
        tangent_vects.set_z_index(1)
        tangent_vects.set_fill(opacity=0.8)
        for vect in tangent_vects:
            vect.set_perpendicular_to_camera(frame)

        self.play(
            dot.animate.set_opacity(1).scale(0.5),
            all_labels.animate.set_stroke(width=0).set_fill(opacity=0.25),
        )
        self.wait()

        lat_line2 = TracedPath(dot.get_center, stroke_color=TEAL, stroke_width=1)
        lat_line2.set_scale_stroke_with_zoom(True)
        self.add(lat_line2)
        self.play(
            uv_tracker.animate.increment_value([30 * DEG, 0]).set_anim_args(rate_func=wiggle),
            FadeOut(lon_line),
            run_time=3
        )
        lat_line2.clear_updaters()
        self.play(GrowArrow(tangent_vects[0]))
        self.wait()

        lon_line2 = TracedPath(dot.get_center, stroke_color=RED, stroke_width=1)
        lon_line2.set_scale_stroke_with_zoom(True)
        self.add(lon_line2)
        self.play(
            tangent_vects[0].animate.set_fill(opacity=0.5).set_anim_args(time_span=(0, 1)),
            uv_tracker.animate.increment_value([0, 30 * DEG]).set_anim_args(rate_func=wiggle),
            FadeOut(lat_line),
            run_time=3
        )
        lon_line2.clear_updaters()
        self.play(GrowArrow(tangent_vects[1]))
        self.play(tangent_vects.animate.set_fill(opacity=1))
        self.wait()

        # Show normal vector
        normal_vect = Arrow(
            point, point + 0.5 * np.cross(u_step, v_step),
            thickness=2,
            buff=0
        )
        normal_vect.set_fill(BLUE, 0.8)
        normal_vect.rotate(90 * DEG, axis=normal_vect.get_vector())

        self.play(
            GrowArrow(normal_vect, time_span=(2, 4)),
            FadeOut(lat_lon_labels, time_span=(0, 2)),
            frame.animate.reorient(-96, 54, 0, (-0.23, -1.08, 0.25), 3.67),
            run_time=8
        )

        # Show a full vector field
        normal_field = get_sphereical_vector_field(
            lambda p: p,
            ThreeDAxes(),
            points=np.array([
                sphere.uv_func(u, v)
                for u in np.arange(0, TAU, TAU / 60)
                for v in np.arange(0, PI, PI / 30)
            ])
        )

        normal_field.save_state()
        normal_field.set_stroke(width=1e-6)

        self.play(
            Restore(normal_field, time_span=(2, 5)),
            frame.animate.reorient(-103, 62, 0, (-0.09, 0.25, 0.23), 7.26),
            run_time=10
        )
        self.wait()
        self.add(self.camera.light_source)

        # Move around light
        light = GlowDot(radius=0.5, color=WHITE)
        light.move_to(self.camera.light_source)
        light.save_state()
        self.camera.light_source.always.move_to(light)

        self.add(self.camera.light_source)
        self.play(
            light.animate.move_to(4 * normalize(light.get_center())),
            run_time=3
        )
        self.play(Rotate(light, TAU, axis=OUT, about_point=ORIGIN, run_time=6))
        self.play(
            FadeOut(normal_field),
            FadeOut(normal_vect),
            Restore(light),
            all_labels.animate.set_fill(opacity=0.5),
            frame.animate.reorient(-63, 66, 0, (-0.09, 0.25, 0.23), 7.26),
            run_time=3
        )

        # Warp sphere
        dot.suspend_updating()
        group = Group(sphere, mesh, lat_line2, lon_line2, all_labels, tangent_vects, dot)
        group.save_state()
        group.target = group.generate_target()
        group.target.rotate(-45 * DEG)
        group.target.scale(0.5)
        group.target.stretch(0.25, 0)
        group.target.shift(RIGHT)
        group.target.apply_complex_function(lambda z: z**3)
        group.target.center()
        group.target.set_height(6)
        group.target.rotate(45 * DEG)

        self.play(Homotopy(homotopy, group, run_time=3))
        self.play(
            MoveToTarget(group),
            frame.animate.reorient(-94, 60, 0, (0.5, 0.84, 0.91), 1.06),
            run_time=8
        )
        self.wait()
        self.play(MoveAlongPath(dot, lat_line2, run_time=5))
        self.play(MoveAlongPath(dot, lon_line2, run_time=5))

        new_normal_vector = Vector(
            0.35 * normalize(np.cross(tangent_vects[0].get_vector(), tangent_vects[1].get_vector())),
            fill_color=BLUE,
            thickness=1
        )
        new_normal_vector.shift(tangent_vects[0].get_start())
        new_normal_vector.set_perpendicular_to_camera(self.frame)
        self.play(
            GrowArrow(new_normal_vector),
            frame.animate.reorient(-125, 52, 0, (0.5, 0.84, 0.91), 1.06),
            run_time=2
        )
        self.wait()
        self.play(
            FadeOut(new_normal_vector, time_span=(0, 1)),
            Restore(group),
            frame.animate.reorient(-78, 66, 0, (-0.13, 0.12, 0.13), 6.54),
            run_time=5
        )

        # Show antipode map
        group = Group(lat_line2, lon_line2, tangent_vects, dot)
        anti_group = group.copy().scale(-1, min_scale_factor=-np.inf, about_point=ORIGIN)

        antipode_lines = VGroup(
            Line(p1, p2)
            for index in [0, 1]
            for p1, p2 in zip(group[index].get_points(), anti_group[index].get_points())
        )
        antipode_lines.set_stroke(YELLOW, 1, 0.1)

        self.play(
            FadeOut(sphere, scale=0.9),
            FadeOut(all_labels),
            VGroup(lat_line2, lon_line2).animate.set_stroke(width=1),
            FadeIn(normal_vect),
            frame.animate.reorient(-93, 55, 0, (-0.26, -0.85, 0.24), 4.27),
            run_time=2
        )

        self.play(
            TransformFromCopy(group, anti_group),
            frame.animate.reorient(-194, 105, 0, (0.7, -0.22, -0.61), 4.64),
            ShowCreation(antipode_lines, lag_ratio=0),
            run_time=5
        )
        self.play(antipode_lines.animate.set_stroke(opacity=0.02))
        self.wait()

        # Map over labels
        all_labels.set_fill(opacity=0.5)
        anti_labels = all_labels.copy().scale(-1, min_scale_factor=-np.inf, about_point=ORIGIN)

        for label in anti_labels:
            label.rotate(PI, axis=np.cross(label.get_center(), IN))

        self.play(FadeIn(all_labels, lag_ratio=0.001, run_time=3))
        self.remove(all_labels)
        self.play(TransformFromCopy(all_labels, anti_labels, lag_ratio=0.0002, run_time=3))
        self.wait()
        self.play(
            MoveAlongPath(dot, anti_group[0], run_time=5),
            anti_group[1].animate.set_stroke(opacity=0.25),
            anti_group[2][1].animate.set_fill(opacity=0.25),
        )
        self.play(
            MoveAlongPath(dot, anti_group[1], run_time=5),
            anti_group[1].animate.set_stroke(opacity=1),
            anti_group[2][1].animate.set_fill(opacity=1),
            anti_group[0].animate.set_stroke(opacity=0.25),
            anti_group[2][0].animate.set_fill(opacity=0.25),
        )
        self.wait()
        self.play(
            anti_group[0].animate.set_stroke(opacity=1),
            anti_group[2][0].animate.set_fill(opacity=1),
        )

        # New normal
        new_normal = normal_vect.copy()
        new_normal.shift(-2 * point)

        self.play(
            GrowArrow(new_normal),
            frame.animate.reorient(-197, 90, 0, (1.16, -0.3, -0.99), 4.64),
            run_time=3
        )
        self.wait()

        # Show reverserd vector field
        anti_normal_field = get_sphereical_vector_field(
            lambda p: -p,
            ThreeDAxes(),
            points=np.array([
                sphere.uv_func(u, v)
                for u in np.arange(0, TAU, TAU / 60)
                for v in np.arange(0, PI, PI / 30)
            ])
        )

        frame.reorient(162, 89, 0, (1.16, -0.3, -0.99), 4.64)
        self.play(
            FadeOut(group),
            FadeOut(antipode_lines),
            FadeIn(anti_normal_field, time_span=(0, 2)),
            frame.animate.reorient(360 - 177, 82, 0, (-0.03, -0.11, 0.86), 9.51),
            run_time=10
        )

        # Show outward vectors again
        self.remove(anti_normal_field)
        self.remove(anti_group)
        self.remove(new_normal)
        self.add(group)
        self.add(normal_field)
        antipode_lines.set_stroke(YELLOW, 1, 0.1)
        self.play(ShowCreation(antipode_lines, lag_ratio=0, run_time=2))
        self.wait()

    def get_lat_lon(self, u, v):
        return np.array([
            v / DEG - 90,
            u / DEG - 180,
        ])
