# ==============================================================================
# Scene:      SingleNullPointHairyBallRevealed
# Source:     videos/_2026/hairy_ball/spheres.py (lines 852-853)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SingleNullPointHairyBallRevealed.py SingleNullPointHairyBallRevealed -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import numpy as np

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


class SingleNullPointHairyBall(InteractiveScene):
    hide_top = True

    def construct(self):
        # Set up
        frame = self.frame
        radius = 3
        sphere = Sphere(radius=radius)
        sphere.set_color(GREY_E, 1)
        sphere.set_shading(0.1, 0.1, 0.3)
        sphere.always_sort_to_camera(self.camera)
        axes = ThreeDAxes((-2, 2), (-2, 2), (-2, 2))
        axes.scale(radius)

        self.camera.light_source.move_to(3 * LEFT + 12 * UP + 3 * OUT)

        frame.reorient(-3, 161, 0)
        self.add(sphere)

        # Add vector field
        def v_func(points3d):
            new_points = stereographic_vector_field(points3d, right_func)
            norms = np.linalg.norm(new_points, axis=1)
            new_points *= 0.2 / norms[:, np.newaxis]
            return new_points

        def out_func(points3d):
            return 0.2 * points3d

        n_points = 50_000
        v_range = (-0.95, 1) if self.hide_top else (-1, 1)
        points = np.array([
            normalize(sphere.uv_func(TAU * random.random(), math.acos(pre_v)))
            for pre_v in np.random.uniform(*v_range, n_points)
        ])
        pre_field, field = fields = [
            get_sphereical_vector_field(
                func, axes, points,
                stroke_width=3,
                mvltss=3,
            )
            for func in [out_func, v_func]
        ]
        for lines in fields:
            lines.set_stroke(BLUE_E, opacity=0.75)
            lines.data['stroke_width'] = 0.5

        q_marks = Tex(R"???", font_size=72)
        q_marks.rotate(-90 * DEG)
        q_marks.move_to(sphere.get_zenith())
        disk = Circle(radius=1)
        disk = Sphere(radius=radius, v_range=(0.9 * PI, PI))
        disk.set_color(BLACK)
        disk.deactivate_depth_test()
        top_q = Group(disk, q_marks)
        top_q.set_z_index(1)

        if not self.hide_top:
            top_q.set_opacity(0)

        self.add(pre_field, sphere)
        self.play(
            ReplacementTransform(pre_field, field, run_time=2),
            frame.animate.reorient(-92, 11, 0).set_anim_args(run_time=7),
            FadeIn(top_q, time_span=(3.5, 5)),
        )
        self.play(
            frame.animate.reorient(-168, 127, 0),
            FadeOut(top_q, time_span=(4.2, 5)),
            run_time=10
        )


class SingleNullPointHairyBallRevealed(SingleNullPointHairyBall):
    hide_top = False
