# ==============================================================================
# Scene:      SurfaceFoldedOverSelf
# Source:     videos/_2026/hairy_ball/spheres.py (lines 1961-2056)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SurfaceFoldedOverSelf.py SurfaceFoldedOverSelf -w -m --fps 15
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


class FlowingWater(InteractiveScene):
    def construct(self):
        # Set up axes
        radius = 2
        frame = self.frame
        axes = ThreeDAxes((-3, 3), (-3, 3), (-3, 3))
        axes.scale(radius)
        frame.reorient(-89, 77, 0)
        frame.add_ambient_rotation(2 * DEG)
        self.add(axes)

        # Add water
        water = self.get_water(sigma0=0.2, n_droplets=1_000_000, opacity=0.1, refresh_ratio=0.015)
        water.scale(0.01, about_point=ORIGIN)
        source_dot = GlowDot(ORIGIN, color=BLUE)

        self.add(source_dot, water)
        water.refresh_sigma_tracker.set_value(0.2)
        water.opacity_tracker.set_value(0.05)
        water.radius_tracker.set_value(0.015)
        frame.reorient(-108, 73, 0, (0.01, 0.06, -0.03), 4.0),
        self.play(
            water.radius_tracker.animate.set_value(0.02),
            water.opacity_tracker.animate.set_value(0.1),
            water.refresh_sigma_tracker.animate.set_value(2.5),
            frame.animate.reorient(-120, 80, 0, ORIGIN, 8.00),
            run_time=10
        )
        self.wait(20)

        # Show full sphere
        sphere = Sphere(radius=radius)
        sphere.set_color(GREY, 0.25)
        sphere.set_shading(0.5, 0.5, 0.5)
        sphere.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(sphere, resolution=(61, 31))
        mesh.set_stroke(WHITE, 1, 0.5)
        mesh.set_z_index(2)

        def get_unit_normal_field(u_range, v_range):
            return get_sphereical_vector_field(
                lambda p: p,
                ThreeDAxes(),
                points=np.array([
                    sphere.uv_func(u, v)
                    for u in u_range
                    for v in v_range
                ])
            )

        normal_field = get_unit_normal_field(
            np.arange(0, TAU, TAU / 60),
            np.arange(0, PI, PI / 30),
        )

        self.play(
            ShowCreation(sphere),
            Write(mesh, lag_ratio=1e-3),
            run_time=2
        )
        self.wait(2)
        self.play(FadeIn(normal_field))
        self.wait(7.2)

        # Show single patch
        u_range_params = (0 * DEG, 15 * DEG, 5 * DEG)
        v_range_params = (120 * DEG, 130 * DEG, 5 * DEG)
        patch = Sphere(
            radius=radius,
            u_range=u_range_params[:2],
            v_range=v_range_params[:2],
        )
        patch.set_color(WHITE, 0.6)

        patch_normals = get_unit_normal_field(np.arange(*u_range_params), np.arange(*v_range_params))

        self.play(
            FadeOut(sphere, time_span=(0, 1)),
            FadeOut(normal_field, time_span=(0, 1)),
            FadeIn(patch, time_span=(0, 1)),
            FadeIn(patch_normals, time_span=(0, 1)),
            mesh.animate.set_stroke(opacity=0.1),
            frame.animate.reorient(19, 55, 0, (1.65, 0.28, 0.98), 2.32),
            water.opacity_tracker.animate.set_value(0.125),
            water.radius_tracker.animate.set_value(0.01),
            run_time=5
        )
        frame.clear_updaters()
        self.wait(8)

        patch_group = Group(patch, patch_normals)

        # Original patch behavior
        self.play(
            Rotate(patch_group, PI, axis=UP),
            run_time=2
        )
        self.wait(2.5)
        self.play(
            Rotate(patch_group, PI, axis=UP, time_span=(0, 1)),
            FadeIn(sphere),
            FadeIn(normal_field),
            frame.animate.reorient(30, 78, 0, (0.19, -0.03, 0.09), 5.67),
            water.opacity_tracker.animate.set_value(0.15),
            water.radius_tracker.animate.set_value(0.015),
            run_time=5
        )
        self.play(FadeOut(patch_group))
        frame.add_ambient_rotation(-1 * DEG)
        self.wait(3)
        self.play(
            FadeOut(normal_field),
            sphere.animate.set_shading(1, 1, 1),
        )
        self.wait(5)

        # Show deformations
        sphere_group = Group(sphere, mesh)

        def alt_uv_func(u, v, params, wiggle_size=1.0, max_freq=4):
            x, y, z = sphere.uv_func(u, v)
            return (
                x + wiggle_size * params[0] * np.cos(max_freq * params[1] * y),
                y + wiggle_size * params[4] * np.cos(max_freq * params[5] * z),
                z + wiggle_size * params[2] * np.cos(max_freq * params[3] * x),
            )

        np.random.seed(3)
        for n in range(20):
            params = np.random.random(6)
            new_sphere = ParametricSurface(
                lambda u, v: alt_uv_func(u, v, params),
                u_range=sphere.u_range,
                v_range=sphere.v_range,
                resolution=sphere.resolution
            )
            new_sphere.match_style(sphere)
            new_mesh = SurfaceMesh(new_sphere, resolution=mesh.resolution)
            new_mesh.match_style(mesh)
            new_group = Group(new_sphere, new_mesh)

            if 10 < n < 13:
                new_group.shift(1.75 * radius * RIGHT)

            self.play(Transform(sphere_group, new_group, run_time=2))
            self.wait(2)

    def get_water(
        self,
        n_droplets=500_000,
        radius=0.02,
        opacity=0.2,
        sigma0=3,
        refresh_sigma=2.5,
        velocity=10,
        refresh_ratio=0.01,
    ):
        points = np.random.normal(0, sigma0, (n_droplets, 3))
        water = DotCloud(points)
        water.set_radius(radius)
        water.set_color(BLUE)
        water.opacity_tracker = ValueTracker(opacity)
        water.radius_tracker = ValueTracker(radius)
        water.refresh_sigma_tracker = ValueTracker(refresh_sigma)
        water.velocity = velocity

        def flow_out(water, dt):
            if dt == 0:
                pass
            points = water.get_points()
            radii = np.linalg.norm(points, axis=1)
            denom = 4 * PI * radii**2
            denom[denom == 0] = 1
            vels = points / denom[:, np.newaxis]
            new_points = points + water.velocity * vels * dt

            n_refreshes = int(refresh_ratio * len(points))
            indices = np.random.randint(0, len(points), n_refreshes)
            new_points[indices] = np.random.normal(0, water.refresh_sigma_tracker.get_value(), (n_refreshes, 3))
            water.set_points(new_points)
            water.set_opacity(water.opacity_tracker.get_value() / np.clip(radii, 1, np.inf))
            water.set_radius(water.radius_tracker.get_value())
            return water

        water.add_updater(flow_out)

        return water

    def rotate_patch(self):
        # to be inserted in "show single patch" above
        patch_group.clear_updaters()
        point = patch.get_center()
        path = Arc(0, PI)
        path.rotate(20 * DEG, RIGHT)
        path.put_start_and_end_on(point, -point)

        patch_group.move_to(path.get_start())
        self.wait(5)
        self.play(
            MoveAlongPath(patch_group, path),
            frame.animate.reorient(-25, 92, 0, (-0.75, -0.96, -0.16), 3.16),
            run_time=5
        )
        self.wait(5)


class SurfaceFoldedOverSelf(FlowingWater):
    def construct(self):
        # Set up axes
        radius = 2
        frame = self.frame
        axes = ThreeDAxes((-3, 3), (-3, 3), (-3, 3))
        axes.scale(radius)
        frame.reorient(-20, 77, 0)
        self.add(axes)

        water = self.get_water()
        self.add(water)

        # Deform sphere
        sphere = Sphere(radius=radius)
        sphere.set_color(GREY, 0.25)
        sphere.set_shading(0.5, 0.5, 0.5)
        sphere.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(sphere, resolution=(61, 31))
        mesh.set_stroke(WHITE, 1, 0.25)
        mesh.set_z_index(2)

        sphere_group = Group(sphere, mesh)
        self.add(sphere_group)
        self.wait(10)

        # Morph
        def inflate(points):
            radii = np.linalg.norm(points, axis=1)
            new_radii = 2.0 * (1 - 1 / (radii + 1))
            return points * (new_radii / radii)[:, np.newaxis]

        sphere_target = sphere_group.copy()
        sphere_target.rotate(90 * DEG, LEFT)
        sphere_target.stretch(0.2, 0)
        sphere_target.stretch(0.5, 1)
        sphere_target.move_to(RIGHT)
        sphere_target.apply_complex_function(lambda z: z**3)
        sphere_target.rotate(90 * DEG, RIGHT)
        sphere_target.shift(radius * OUT)
        sphere_target.apply_points_function(inflate, about_point=ORIGIN)
        sphere_target.replace(sphere)

        sphere_group.save_state()
        self.play(
            frame.animate.reorient(-25, 76, 0, (-0.13, 0.29, 0.85), 3.38).set_anim_args(time_span=(2, 5)),
            Transform(sphere_group, sphere_target),
            water.radius_tracker.animate.set_value(0.01),
            water.opacity_tracker.animate.set_value(0.1),
            run_time=5
        )
        frame.add_ambient_rotation(0.5 * DEG)

        # Show vectors
        direction = OUT + 0.2 * LEFT

        vect = Vector(0.35 * direction, fill_color=GREEN)
        vect.set_perpendicular_to_camera(frame)
        vect.shift(1.1 * direction)
        vect.set_fill(opacity=0.75)

        vect1 = vect.copy()
        vect2 = vect.copy().shift(0.4 * direction).set_color(RED)
        vect3 = vect.copy().shift(0.8 * direction)

        dashed_line = DashedLine(ORIGIN, 5 * direction, dash_length=0.02)
        dashed_line.set_stroke(WHITE, 4)
        dashed_line_ghost = dashed_line.copy()
        dashed_line_ghost.set_stroke(opacity=0.25)
        dashed_line.apply_depth_test()

        self.play(
            ShowCreation(dashed_line, run_time=5),
            ShowCreation(dashed_line_ghost, run_time=5),
        )
        self.wait()
        self.play(
            GrowArrow(vect1),
            GrowArrow(vect3),
        )
        self.wait(3)
        self.play(GrowArrow(vect2))
        self.wait(4)
        self.play(
            FadeOut(VGroup(vect1, vect2, vect3)),
            FadeOut(dashed_line),
            FadeOut(dashed_line_ghost),
        )

        # Shift back
        frame.clear_updaters()
        self.play(
            Restore(sphere_group),
            frame.animate.reorient(10, 78, 0, ORIGIN, 7),
            run_time=7
        )
