# ==============================================================================
# Scene:      PairsOfNullPoints
# Source:     videos/_2026/hairy_ball/spheres.py (lines 856-969)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PairsOfNullPoints.py PairsOfNullPoints -w -m --fps 15
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


class PairsOfNullPoints(InteractiveScene):
    def construct(self):
        # Set up
        frame = self.frame
        radius = 3
        sphere_scale = 0.99
        axis_range = (-4, 4)

        sphere = Sphere(radius=sphere_scale * radius)
        sphere.set_color(GREY_D, 0.5)
        sphere.always_sort_to_camera(self.camera)
        axes = ThreeDAxes(axis_range, axis_range, axis_range)
        axes.scale(radius)

        frame.reorient(-155, 74, 0)
        self.add(axes, sphere)

        # Vector field
        def source_and_sink(points2d, offset=-3):
            x, y = points2d.T
            return np.array([x - offset, y]).T

        def twirl_func(points2d, offset=-3):
            x, y = points2d.T
            return np.array([-y, x - offset]).T

        rotation = np.identity(3)[:, [0, 2, 1]]

        field = self.get_spherical_field(axes, twirl_func, rotation=rotation)
        offset_tracker = ValueTracker(-1)

        self.add(sphere, field)
        frame.reorient(-136, 77, 0, (0.91, 0.31, 0.79), 12.58)
        self.play(
            frame.animate.reorient(-177, 80, 0, (0.0, 0.0, 0.0), 8),
            run_time=4
        )
        frame.add_ambient_rotation(1 * DEG)

        # Change the field around
        new_params = [
            (rotation_matrix_transpose(90 * DEG, UP), -5),
            (rotation_matrix_transpose(30 * DEG, DOWN), -2),
            (rotation_matrix_transpose(120 * DEG, LEFT), 3),
            (rotation, -1),
        ]
        for new_rot, offset in new_params:
            new_field = self.get_spherical_field(
                axes, lambda ps: twirl_func(ps, offset), rotation=new_rot
            )
            self.play(Transform(field, new_field, run_time=2))

        self.play(
            offset_tracker.animate.set_value(-3),
            UpdateFromFunc(
                field,
                lambda m: m.become(
                    self.get_spherical_field(axes, lambda ps: twirl_func(ps, offset_tracker.get_value()), rotation=rotation)
                )
            ),
            run_time=4
        )

        # Show some flow
        streamlines = self.get_streamlines(field, axes, radius)
        self.add(streamlines)
        self.wait(8)

        # New field
        field2 = self.get_spherical_field(axes, source_and_sink)
        streamlines2 = self.get_streamlines(field2, axes, radius, density=100)

        self.play(FadeOut(streamlines))
        self.play(Transform(field, field2))
        self.play(FadeIn(streamlines2))
        self.wait(8)

    def get_streamlines(self, field, axes, radius, density=100):
        streamlines = SphereStreamLines(
            lambda p: field.func(np.array(p).reshape(-1, 3)).flatten(), axes,
            density=density,
            solution_time=1.0,
            dt=0.05,
        )
        streamlines.scale(radius, about_point=ORIGIN)
        streamlines.set_stroke(WHITE, 1, 0.5)
        animated_lines = AnimatedStreamLines(streamlines, rate_multiple=0.2)
        animated_lines.apply_depth_test()
        return animated_lines

    def get_spherical_field(
        self,
        axes,
        plane_func,
        n_sample_points=2000,
        stroke_width=2,
        rotation=np.identity(3),
    ):
        def v_func(points3d):
            rot_points = np.dot(points3d, rotation)
            new_points = stereographic_vector_field(rot_points, plane_func)
            norms = np.linalg.norm(new_points, axis=1)
            new_points *= 1.0 / norms[:, np.newaxis]
            new_points = np.dot(new_points, rotation.T)
            return new_points

        sample_points = fibonacci_sphere(n_sample_points)
        field = get_sphereical_vector_field(
            v_func, axes, sample_points,
            stroke_width=stroke_width
        )
        field.set_flat_stroke(False)

        return field
