# ==============================================================================
# Scene:      InsideOutWithNormalField
# Source:     videos/_2026/hairy_ball/spheres.py (lines 2059-2123)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InsideOutWithNormalField.py InsideOutWithNormalField -w -m --fps 15
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


class InsideOutWithNormalField(InteractiveScene):
    def construct(self):
        # Axes and plane
        radius = 3
        frame = self.frame
        axes = ThreeDAxes()
        plane = NumberPlane((-8, 8), (-8, 8))
        plane.background_lines.set_stroke(GREY_C, 1)
        plane.faded_lines.set_stroke(GREY_C, 0.5, 0.5)
        plane.apply_depth_test()
        axes.apply_depth_test()
        self.add(axes, plane)

        # Add sphere
        outer_sphere = Sphere(radius=radius)
        inner_sphere = Sphere(radius=0.99 * radius)
        outer_sphere.set_color(BLUE_E, 1)
        inner_sphere.set_color(interpolate_color(GREY_BROWN, BLACK, 0.5), 1)
        for sphere in [inner_sphere, outer_sphere]:
            sphere.always_sort_to_camera(self.camera)
            sphere.set_shading(0.2, 0.2, 0.1)
        mesh = SurfaceMesh(outer_sphere, resolution=(61, 31))
        mesh.set_stroke(WHITE, 1, 0.5)
        mesh.set_z_index(2)

        def get_unit_normal_field(u_range, v_range, sign=1):
            return get_sphereical_vector_field(
                lambda p: sign * p,
                axes,
                points=np.array([
                    sphere.uv_func(u, v)
                    for u in u_range
                    for v in v_range
                ]),
                color=BLUE_D,
                stroke_width=3
            )

        u_range = np.arange(0, TAU, TAU / 30)
        v_range = np.arange(0, PI, PI / 15)
        outer_normals = get_unit_normal_field(u_range, v_range)
        inner_normals = get_unit_normal_field(u_range, v_range, -1)

        sign_tracker = ValueTracker(1)
        outer_normals.add_updater(lambda m: m.set_stroke(opacity=float(sign_tracker.get_value() > 0)))
        inner_normals.add_updater(lambda m: m.set_stroke(opacity=float(sign_tracker.get_value() < 0)))

        sphere_group = Group(inner_sphere, outer_sphere, mesh, outer_normals, inner_normals)
        sphere_group.set_clip_plane(UP, 0)
        frame.reorient(-23, 72, 0)
        self.add(sphere_group, axes)

        # Inversion homotopy
        def homotopy(x, y, z, t, scale=-1):
            p = np.array([x, y, z])
            power = 1 + 0.2 * (x / radius)
            return interpolate(p, scale * p, t**power)

        frame.add_ambient_rotation(3 * DEG)
        self.play(
            Homotopy(homotopy, sphere_group),
            sign_tracker.animate.set_value(-1),
            run_time=5
        )
        self.wait(3)
