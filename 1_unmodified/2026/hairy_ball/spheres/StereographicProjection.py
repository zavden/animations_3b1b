# ==============================================================================
# Scene:      StereographicProjection
# Source:     videos/_2026/hairy_ball/spheres.py (lines 464-742)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StereographicProjection.py StereographicProjection -w -m --fps 15
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


def inv_streographic_proj(points2d):
    u, v = points2d.T
    norm_squared = u * u + v * v
    denom = 1 + norm_squared
    return np.array([
        2 * u / denom,
        2 * v / denom,
        (norm_squared - 1) / denom,
    ]).T


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


class StereographicProjection(InteractiveScene):
    def construct(self):
        # Set up
        frame = self.frame
        x_max = 20
        axes = ThreeDAxes((-x_max, x_max), (-x_max, x_max), (-2, 2))
        plane = NumberPlane((-x_max, x_max), (-x_max, x_max))
        plane.background_lines.set_stroke(BLUE, 1, 0.5)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.25)
        axes.apply_depth_test()
        plane.apply_depth_test()

        sphere = Sphere(radius=1)
        sphere.set_opacity(0.5)
        sphere.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(sphere)
        mesh.set_stroke(WHITE, 1, 0.25)

        self.add(sphere, mesh, axes, plane)
        frame.reorient(-15, 64, 0, (0.0, 0.1, -0.09), 4.0)

        # Show the 2d cross section
        frame.clear_updaters()
        sphere.set_clip_plane(UP, 1)
        n_dots = 20
        sample_points = np.array([
            math.cos(theta) * OUT + math.sin(theta) * RIGHT
            for theta in np.linspace(0, TAU, n_dots + 2)[1:-1]
        ])
        sphere_dots, plane_dots, proj_lines = self.get_dots_and_lines(sample_points)

        self.play(
            sphere.animate.set_clip_plane(UP, 0),
            frame.animate.reorient(-43, 74, 0, (0.0, 0.0, -0.0), 3.50),
            FadeIn(sphere_dots, time_span=(1, 2)),
            ShowCreation(proj_lines, lag_ratio=0, time_span=(1, 2)),
            run_time=2
        )
        frame.add_ambient_rotation(2 * DEG)

        sphere_dot_ghosts = sphere_dots.copy().set_opacity(0.5)
        self.remove(sphere_dots)
        self.add(sphere_dot_ghosts)
        self.play(
            TransformFromCopy(sphere_dots, plane_dots, lag_ratio=0.5, run_time=10),
        )
        self.wait(3)

        planar_group = Group(sphere_dot_ghosts, plane_dots, proj_lines)

        # Show more points on the sphere
        sample_points = fibonacci_sphere(200)
        sphere_dots, plane_dots, proj_lines = self.get_dots_and_lines(sample_points)

        self.play(
            sphere.animate.set_clip_plane(UP, -1),
            frame.animate.reorient(-65, 73, 0, (-0.09, -0.01, -0.15), 5.08),
            ShowCreation(proj_lines, lag_ratio=0),
            FadeOut(planar_group),
            run_time=2,
        )
        self.wait(4)
        self.play(FadeIn(sphere_dots))
        self.wait(2)

        sphere_dot_ghosts = sphere_dots.copy().set_opacity(0.5)
        self.remove(sphere_dots)
        self.add(sphere_dot_ghosts)

        self.play(
            TransformFromCopy(sphere_dots, plane_dots, run_time=3),
        )
        self.wait(3)

        # Inverse projection
        plane.insert_n_curves(100)
        plane.save_state()
        proj_plane = plane.copy()
        proj_plane.apply_points_function(lambda p: inv_streographic_proj(p[:, :2]))
        proj_plane.make_smooth()
        proj_plane.background_lines.set_stroke(BLUE, 2, 1)
        proj_plane.faded_lines.set_stroke(BLUE, 1, 0.5)

        self.play(
            Transform(plane_dots, sphere_dot_ghosts),
            FadeOut(sphere_dot_ghosts, scale=0.9),
            Transform(plane, proj_plane),
            proj_lines.animate.set_stroke(opacity=0.2),
            run_time=4,
        )
        self.play(
            frame.animate.reorient(-20, 38, 0, (-0.04, -0.03, 0.13), 3.54),
            run_time=5
        )
        self.wait(5)
        self.play(
            frame.animate.reorient(-27, 73, 0, (-0.03, 0.03, 0.04), 5.27),
            Restore(plane),
            FadeOut(plane_dots),
            run_time=5
        )
        self.wait(2)

        # Show a vector field
        xy_field = VectorField(lambda ps: np.array([RIGHT for p in ps]), plane)
        xy_field.set_stroke(BLUE)
        xy_field.save_state()
        xy_field.set_stroke(width=1e-6)

        self.play(Restore(xy_field))
        self.wait(5)

        # Project the vector field up
        proj_field = xy_field.copy()
        proj_field.apply_points_function(lambda p: inv_streographic_proj(p[:, :2]), about_point=ORIGIN)
        proj_field.replace(sphere)
        proj_plane.background_lines.set_stroke(BLUE, 1, 0.5)
        proj_plane.faded_lines.set_stroke(BLUE, 0.5, 0.25)
        proj_plane.axes.set_stroke(WHITE, 0)

        self.play(
            Transform(plane, proj_plane),
            Transform(xy_field, proj_field),
            run_time=5,
        )
        self.play(
            frame.animate.reorient(-35, 31, 0, (0.05, 0.22, 0.22), 1.59),
            FadeOut(proj_lines),
            run_time=10
        )
        self.wait(8)

        # Show the flow (Maybe edit as a simple split-screen)
        proto_stream_lines = VGroup(
            Line([x, y, 0], [x + 20, y, 0]).insert_n_curves(25)
            for x in range(-100, 100, 10)
            for y in np.arange(-100, 100, 0.25)
        )
        for line in proto_stream_lines:
            line.virtual_time = 1
        proto_stream_lines.set_stroke(WHITE, 2, 0.8)
        proto_stream_lines.apply_points_function(lambda p: inv_streographic_proj(p[:, :2]), about_point=ORIGIN)
        proto_stream_lines.scale(1.01)
        proto_stream_lines.make_smooth()
        animated_lines = AnimatedStreamLines(proto_stream_lines, rate_multiple=0.2)

        sphere.set_color(GREY_E, 1)
        sphere.set_clip_plane(UP, 1)
        sphere.set_height(1.98).center()
        xy_field.apply_depth_test()
        animated_lines.apply_depth_test()
        self.add(sphere, mesh, plane, animated_lines, xy_field)
        self.play(
            FadeIn(sphere),
            FadeOut(xy_field),
            plane.animate.fade(0.25),
            xy_field.animate.set_stroke(opacity=0.5),
            frame.animate.reorient(-30, 29, 0, ORIGIN, 3.0),
            run_time=3
        )
        self.wait(30)
        return

    def get_dots_and_lines(self, sample_points, color=YELLOW, radius=0.025, stroke_opacity=0.35):
        sphere_dots = Group(TrueDot(point) for point in sample_points)
        for dot in sphere_dots:
            dot.make_3d()
            dot.set_color(color)
            dot.set_radius(radius)

        plane_dots = sphere_dots.copy().apply_points_function(stereographic_proj)
        proj_lines = VGroup(
            VGroup(
                Line(OUT, dot.get_center())
                for dot in dots
            )
            for dots in [plane_dots, sphere_dots]
        )
        proj_lines.set_stroke(color, 1, stroke_opacity)

        return sphere_dots, plane_dots, proj_lines

    def flow_with_projection_insertion(self):
        # For an insertion
        frame.clear_updaters()
        frame.reorient(-18, 77, 0, (-0.04, 0.04, 0.09), 5.43)
        frame.clear_updaters()
        frame.add_ambient_rotation(1 * DEG)
        sphere.set_clip_plane(UP, 2)
        sphere.set_color(GREY_D, 0.5)
        xy_field.apply_depth_test()
        xy_field.set_stroke(opacity=0.)
        proj_lines.set_stroke(opacity=0)
        proj_plane.axes.set_stroke(width=1, opacity=0.5)
        self.clear()
        sphere.scale(0.99)
        self.add(axes, xy_field, proj_lines, sphere, plane, frame)

        # Particles
        n_samples = 50_000
        x_max = axes.x_range[1]
        sample_points = np.random.uniform(-x_max, x_max, (n_samples, 3))
        sample_points[:, 2] = 0
        particles = DotCloud(sample_points)
        particles.set_radius(0.015)
        particles.set_color(BLUE)
        particles.make_3d()

        particle_opacity_tracker = ValueTracker(1)
        proj_particle_radius_tracker = ValueTracker(0.01)

        proj_particles = particles.copy()
        proj_particles.set_opacity(1)

        x_vel = 0.5

        def update_particles(particles, dt):
            particles.shift(dt * x_vel * RIGHT)
            points = particles.get_points()
            points[points[:, 0] > x_max, 0] -= 2 * x_max
            particles.set_points(points)
            particles.set_opacity(particle_opacity_tracker.get_value())

            sphere_points = inv_streographic_proj(points[:, :2])
            zs = sphere_points[:, 2]
            proj_particles.set_points(sphere_points)
            proj_particles.set_radius((proj_particle_radius_tracker.get_value() * (1.5 - zs)).reshape(-1, 1))

        particles.add_updater(update_particles)
        self.add(particles, sphere)
        self.wait(7)

        # Project
        moving_particles = particles.copy()
        moving_particles_opacity_tracker = ValueTracker(0)
        moving_particles.add_updater(lambda m: m.set_opacity(moving_particles_opacity_tracker.get_value()))

        field = get_sphereical_vector_field(
            lambda p3d: stereographic_vector_field(p3d, right_func),
            axes,
            fibonacci_sphere(1000),
            stroke_width=0.5
        )
        field.set_stroke(WHITE, opacity=0.5)

        self.play(proj_lines.animate.set_opacity(0.4))
        self.play(
            particle_opacity_tracker.animate.set_value(0.15),
            Transform(moving_particles, proj_particles),
            moving_particles_opacity_tracker.animate.set_value(1),
            run_time=5
        )
        self.remove(moving_particles)
        self.add(sphere, particles, proj_particles)
        self.play(
            proj_lines.animate.set_opacity(0.1),
            frame.animate.reorient(-30, 29, 0, ORIGIN, 3.0),
            proj_particle_radius_tracker.animate.set_value(0.0075),
            FadeIn(field),
            run_time=3
        )
        self.wait(15)


    def old(self):
        earth = TexturedSurface(sphere, "EarthTextureMap")
        earth.set_opacity(1)

        earth_group = Group(earth)
        earth_group.save_state()
        proj_earth = earth_group.copy()
        proj_earth.apply_points_function(stereographic_proj)
        proj_earth.interpolate(proj_earth, earth_group, 0.01)

        self.remove(earth_group)
        self.play(TransformFromCopy(earth_group, proj_earth), run_time=3)
        self.wait()
        self.remove(proj_earth)
        self.play(TransformFromCopy(proj_earth, earth_group), run_time=3)
