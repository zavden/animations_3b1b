# ==============================================================================
# Scene:      InsideOut
# Source:     videos/_2026/hairy_ball/spheres.py (lines 1122-1352)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InsideOut.py InsideOut -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import numpy as np

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
