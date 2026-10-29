# ==============================================================================
# Scene:      IntroduceVectorField
# Source:     videos/_2026/hairy_ball/spheres.py (lines 211-461)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceVectorField.py IntroduceVectorField -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import numpy as np

def fibonacci_sphere(samples=1000):
    """
    Create uniform-ish points on a sphere

    Parameters
    ----------
    samples : int
        Number of points to create. The default is 1000.

    Returns
    -------
    points : NumPy array
        Points on the unit sphere.

    """

    # Define the golden angle
    phi = np.pi * (np.sqrt(5) - 1)

    # Define y-values of points
    pos = np.array(range(samples), ndmin=2)
    y = 1 - (pos / (samples - 1)) * 2

    # Define radius of cross-section at y
    radius = np.sqrt(1 - y * y)

    # Define the golden angle increment
    theta = phi * pos

    # Define x- and z- values of poitns
    x = np.cos(theta) * radius
    z = np.sin(theta) * radius

    # Merge together x,y,z
    points = np.concatenate((x, y, z))

    # Transpose to get coordinates in right place
    points = np.transpose(points)

    return points


def stereographic_proj(points3d, epsilon=1e-10):
    x, y, z = points3d.T

    denom = 1 - z
    denom[np.abs(denom) < epsilon] = np.inf
    return np.array([x / denom, y / denom, 0 * z]).T


def right_func(points):
    return np.repeat([[1, 0]], len(points), axis=0)


def stereographic_vector_field(points3d, vector_field_2d):
    points2d = stereographic_proj(points3d)[:, :2]
    vects2d = vector_field_2d(points2d)
    u, v = points2d.T
    vect_u, vect_v = vects2d.T

    # Compute Jacobian
    r_squared = u**2 + v**2
    denom = 1 + r_squared
    denom_squared = denom**2

    # For x = 2u / (1 + u² + v²):
    dx_du = 2 * (1 + v**2 - u**2) / denom_squared
    dx_dv = -4 * u * v / denom_squared

    # For y = 2v / (1 + u² + v²):
    dy_du = -4 * u * v / denom_squared
    dy_dv = 2 * (1 + u**2 - v**2) / denom_squared

    # For z = (u² + v² - 1) / (1 + u² + v²):
    dz_du = 4 * u / denom_squared
    dz_dv = 4 * v / denom_squared

    # Apply the Jacobian: [v_x, v_y, v_z]^T = J × [v_u, v_v]^T
    vect_x = dx_du * vect_u + dx_dv * vect_v
    vect_y = dy_du * vect_u + dy_dv * vect_v
    vect_z = dz_du * vect_u + dz_dv * vect_v

    return np.array([vect_x, vect_y, vect_z]).T


def rotation_field(points3d, axis=IN):
    return np.cross(points3d, axis)


def flatten_field(points3d, vector_field_3d):
    vects = vector_field_3d(points3d)
    norms = normalize_along_axis(points3d, 1)
    return np.cross(vects, norms)


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


class SphereStreamLines(StreamLines):
    def __init__(self, func, coordinate_system, density=50, sample_coords=None, **kwargs):
        self.sample_coords = sample_coords
        super().__init__(func, coordinate_system, density=density, **kwargs)

    def get_sample_coords(self):
        if self.sample_coords is None:
            coords = fibonacci_sphere(int(4 * PI * self.density))
        else:
            coords = self.sample_coords
        return coords

    def draw_lines(self):
        super().draw_lines()
        for submob in self.submobjects:
            submob.set_points(normalize_along_axis(submob.get_points(), 1))
        return self


class IntroduceVectorField(InteractiveScene):
    def construct(self):
        # Set up sphere
        frame = self.frame
        self.camera.light_source.move_to([0, -10, 10])
        radius = 3
        axes = ThreeDAxes((-2, 2), (-2, 2), (-2, 2))
        axes.scale(radius)
        sphere = Sphere(radius=radius)
        sphere.set_color(BLUE_B, 0.3)
        sphere.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(sphere, (51, 25))
        mesh.set_stroke(WHITE, 1, 0.15)

        frame.reorient(0, 90, 0)
        self.play(
            frame.animate.reorient(30, 65, 0),
            ShowCreation(sphere),
            Write(mesh, time_span=(1, 3), lag_ratio=1e-2),
            run_time=3
        )

        # Tangent plane
        v_tracker = Point()
        v_tracker.move_to(radius * OUT)

        def place_on_vect(mobject):
            matrix = z_to_vector(v_tracker.get_center())
            mobject.set_points(np.dot(mobject.points_at_zenith, matrix.T))

        v_dot = Dot(radius=0.05)
        v_dot.set_fill(YELLOW)

        plane = Square(side_length=2 * radius)
        plane.set_stroke(WHITE, 1)
        plane.set_fill(GREY, 0.5)

        for mob in [plane, v_dot]:
            mob.move_to(radius * OUT)
            mob.points_at_zenith = mob.get_points().copy()
            mob.add_updater(place_on_vect)

        self.play(
            VFadeIn(v_dot),
            v_tracker.animate.move_to(radius * normalize(RIGHT + OUT)),
            run_time=2
        )
        self.wait()
        plane.update()
        plane.suspend_updating()
        self.play(
            FadeIn(plane),
            frame.animate.reorient(13, 78, 0),
            run_time=2
        )
        self.play(frame.animate.reorient(53, 60, 0, (-0.29, 0.09, 0.31), 8.97), run_time=2)
        self.wait()

        # Show one vector
        def v_func(points3d):
            v1 = stereographic_vector_field(points3d, right_func)
            v2 = normalize_along_axis(rotation_field(points3d, RIGHT), 1)
            v3 = normalize_along_axis(rotation_field(points3d, RIGHT + IN), 1)
            return (3 * v1 + v2 + v3) / 6

        def vector_field_3d(points3d):
            x, y, z = points3d.T
            return np.array([
                np.cos(3 * x) * np.sin(y),
                np.cos(5 * z) * np.sin(x),
                -z**2 + x,
            ]).T

        def alt_v_func(points3d):
            return normalize_along_axis(flatten_field(points3d, vector_field_3d), 1)

        def get_tangent_vect():
            origin = v_tracker.get_center()
            vector = Arrow(origin, origin + radius * v_func(normalize(origin).reshape(1, -1)).flatten(), buff=0, thickness=3)
            vector.set_fill(BLUE)
            vector.set_perpendicular_to_camera(frame)
            return vector

        tangent_vect = get_tangent_vect()
        self.add(plane, tangent_vect, v_dot)
        self.play(GrowArrow(tangent_vect))
        self.play(Rotate(tangent_vect, TAU, axis=v_tracker.get_center(), about_point=tangent_vect.get_start(), run_time=2))
        self.wait()

        # Show more vectors
        plane.resume_updating()
        tangent_vect.add_updater(lambda m: m.match_points(get_tangent_vect()))
        og_vect = rotate_vector(v_tracker.get_center(), 10 * DEG, axis=DOWN)
        v_tracker.clear_updaters()
        v_tracker.add_updater(lambda m, dt: m.rotate(60 * DEG * dt, axis=og_vect, about_point=ORIGIN))
        v_tracker.add_updater(lambda m, dt: m.rotate(1 * DEG * dt, axis=RIGHT, about_point=ORIGIN))

        frame.clear_updaters()
        frame.add_ambient_rotation(-2.5 * DEG)

        self.wait(2)

        field = self.get_vector_field(axes, v_func, 4000, start_point=v_tracker.get_center())
        self.add(field, plane, v_tracker, tangent_vect, v_dot)
        self.play(
            ShowCreation(field),
            run_time=5
        )
        self.wait(4)
        self.play(
            FadeOut(plane),
            FadeOut(tangent_vect),
            FadeOut(v_dot),
            frame.animate.reorient(0, 59, 0, (-0.03, 0.15, -0.08), 6.80),
            run_time=4
        )
        self.wait(5)

        # Show denser field
        dots, dense_dots = [
            DotCloud(fibonacci_sphere(num), radius=0.01)
            for num in [4000, 400_000]
        ]
        for mob in [dots, dense_dots]:
            mob.make_3d()
            mob.set_color(WHITE)
            mob.scale(radius * 1.01)

        dense_field = self.get_vector_field(axes, v_func, 50_000, mvltss=5.0)
        dense_field.set_stroke(opacity=0.35)

        dots.set_radius(0.02)
        dense_dots.set_radius(0.01)

        self.play(ShowCreation(dots, run_time=3))
        self.wait()
        self.play(
            FadeOut(dots, time_span=(1.5, 2.5)),
            FadeOut(field, time_span=(2.5, 3)),
            ShowCreation(dense_field),
            run_time=3
        )
        frame.clear_updaters()
        self.play(frame.animate.reorient(-66, 52, 0, (-0.51, 0.27, 0.2), 2.81), run_time=4)
        self.wait()

        # Show plane and tangent vector again
        field.save_state()
        field.set_stroke(width=1e-6)
        self.play(
            dense_field.animate.set_stroke(width=1e-6),
            Restore(field, time_span=(1, 3)),
            frame.animate.reorient(48, 54, 0, (-2.74, -2.49, -0.1), 11.93),
            VFadeIn(plane),
            VFadeIn(tangent_vect),
            run_time=5
        )
        self.wait(5)

        v_tracker.clear_updaters()
        null_point = 3 * normalize(np.array([-1, -0.25, 0.8]))
        self.play(
            v_tracker.animate.move_to(null_point),
            frame.animate.reorient(-43, 55, 0, (-2.42, 2.76, -0.55), 9.22),
            run_time=3
        )
        self.remove(tangent_vect)
        v_dot.update()
        self.play(
            FadeIn(v_dot, scale=0.25),
            FadeOut(plane, scale=0.25),
        )
        self.wait()

        # Define streamlines
        static_stream_lines = SphereStreamLines(
            lambda p: v_func(np.array(p).reshape(-1, 3)).flatten(),
            axes,
            density=400,
            stroke_width=2,
            magnitude_range=(0, 10),
            solution_time=1,
        )
        static_stream_lines.scale(radius)
        static_stream_lines.set_stroke(BLUE_B, 3, 0.8)
        stream_lines = AnimatedStreamLines(static_stream_lines, lag_range=10, rate_multiple=0.5)
        stream_lines.apply_depth_test()

        # Show the earth
        earth = TexturedSurface(sphere, "EarthTextureMap", "NightEarthTextureMap")
        earth.rotate(-90 * DEG, IN)
        earth.scale(1.001)
        frame.add_ambient_rotation(2 * DEG)

        self.add(sphere, earth, stream_lines, mesh, field)
        self.play(
            FadeOut(v_dot),
            FadeIn(earth, time_span=(0, 3)),
            field.animate.set_stroke(opacity=0.25).set_anim_args(time_span=(0, 2)),
            frame.animate.reorient(-90, 74, 0, (-1.37, 0.04, 0.37), 5.68),
        )
        self.wait(10)

        # Zoom in to null point
        frame.clear_updaters()
        dense_field = self.get_vector_field(axes, v_func, 10_000)
        dense_field.set_stroke(opacity=0.35)
        self.play(
            FadeOut(field, run_time=2),
            FadeIn(dense_field, run_time=2),
            frame.animate.reorient(-69, 54, 0, (-0.01, 0.19, -0.04), 4.81),
            run_time=5
        )
        self.wait(3)
        self.play(
            frame.animate.reorient(129, 70, 0, (-0.18, 0.18, -0.1), 8.22),
            run_time=20
        )
        self.wait(10)

    def get_vector_field(self, axes, v_func, n_points, start_point=None, mvltss=1.0, random_order=False):
        points = fibonacci_sphere(n_points)

        if start_point is not None:
            points = points[np.argsort(np.linalg.norm(points - start_point.reshape(-1, 3), axis=1))]
        if random_order:
            indices = list(range(len(points)))
            random.shuffle(indices)
            points = points[indices]

        alpha = clip(inverse_interpolate(10_000, 1000, n_points), 0, 1)
        stroke_width = interpolate(1, 3, alpha**2)

        return get_sphereical_vector_field(v_func, axes, points, mvltss=mvltss, stroke_width=stroke_width)

    def old(self):
        # Vary the density
        density_tracker = ValueTracker(2000)
        field.add_updater(
            lambda m: m.become(self.get_vector_field(int(density_tracker.get_value()), axes, v_func))
        )
        self.add(field)
        field.resume_updating()
        frame.suspend_updating()
        self.play(
            density_tracker.animate.set_value(50_000),
            frame.animate.reorient(-30, 50, 0, (-0.07, 0.02, 0.36), 3.01),
            run_time=5,
        )
        field.suspend_updating()
        self.wait(3)
