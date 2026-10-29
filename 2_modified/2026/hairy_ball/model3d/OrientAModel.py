# ==============================================================================
# Scene:      OrientAModel
# Source:     videos/_2026/hairy_ball/model3d.py (lines 111-460)
# Category:   2 · Renders with modifications
# Includes code copied from: _2026/hairy_ball/spheres.py
#
# Run from this folder:
#     manimgl OrientAModel.py OrientAModel -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - S3Viking: TexturedGeometry only defines LightTexture but the textured_surface.wgsl shader always reads DarkTexture (shader compile error); the same texture is reused as DarkTexture.
#   - S3Viking: TexturedGeometry does not call Surface.__init__ and lacks sort_to_camera and opaque_version, which the renderer reads on every frame; they are initialized to False and 0.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/models/s3_viking/s3.obj  (placeholder model: small airplane with 168 vertices)
#   - _lib/assets/models/s3_viking/texture.png  (placeholder texture: gray with red and green wing tips)
#
# Notes:
#   The Lockheed S-3 Viking model (s3_viking/s3.obj) comes from Grant's Dropbox. The scene only uses it as an airplane that orients and rotates along trajectories (S3Viking.reposition places nose = +x, wing = y, up = z), so a simple small airplane works (fuselage, nose cone, wings, tail, stabilizer and two engines) with differently colored wing tips so the rotation is visible. Convention of the raw OBJ, the same one S3Viking assumes: nose at -x, up +y, wings along z. Generated with _lib/assets/generated/2026/hairy_ball/make_s3_viking_placeholder.py. The face trimming by tube_index = 38950 does not affect the placeholder model (it has fewer vertices).
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import numpy as np


# ----- From _2026/hairy_ball/spheres.py -----

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



# ----- From _2026/hairy_ball/model3d.py -----

def faulty_perp(heading):
    return normalize(np.cross(heading, -OUT))


def get_position_vectors(trajectory, prop, d_prop=1e-4, use_curvature=False):
    if use_curvature:
        d_prop = 1e-2
    p0 = trajectory.pfp(clip(prop - d_prop, 0, 1))
    p1 = trajectory.pfp(prop)
    p2 = trajectory.pfp(clip(prop + d_prop, 0, 1))
    heading = normalize(p2 - p0)
    if use_curvature:
        acc = normalize(p2 - 2 * p1 + p0)
        top_vect = acc - IN
        wing_vect = normalize(np.cross(top_vect, heading))
    else:
        wing_vect = faulty_perp(heading)
    return (p1, heading, wing_vect)


class S3Viking(TexturedGeometry):
    offset = np.array([-0.2, 0, 0.2])

    def __init__(self, height=1):
        full_model = ThreeDModel("s3_viking/s3.obj")
        plane = full_model[-1]
        super().__init__(plane.geometry, plane.texture_file)
        # CHANGE: the textured_surface.wgsl shader always reads DarkTexture, but TexturedGeometry only defines LightTexture (shader compile error); the same texture is reused
        self.textures["DarkTexture"] = self.textures["LightTexture"].copy()
        # CHANGE: TexturedGeometry does not call Surface.__init__ and lacks sort_to_camera and opaque_version, which the renderer reads on every frame
        self.sort_to_camera = False
        self.opaque_version = 0
        self.set_height(height)
        self.apply_depth_test()
        self.rotate(PI).rotate(PI / 2, LEFT)

        # Trim, a bit hacky. Keep the faces whose every corner is a point of the mesh
        # below the index, vertex_indices saying which point each record came from
        tube_index = 38_950
        keep = (self.vertex_indices < tube_index).reshape((-1, 3)).all(1).repeat(3)
        self.vertex_indices = self.vertex_indices[keep]
        self.set_data(self.data[keep])
        self.refresh_bounding_box()
        self.move_to(height * self.offset)

        # Remoember position
        self.initial_points = self.get_points().copy()

    def reposition(self, center, heading, wing_vect):
        unit_heading = normalize(heading)
        roof_vect = normalize(np.cross(heading, wing_vect))
        true_wing = normalize(np.cross(roof_vect, heading))
        rot_mat_T = np.array([unit_heading, true_wing, roof_vect])

        self.set_points(np.dot(self.initial_points, rot_mat_T) + center)

    def place_on_path(self, trajectory, prop, use_curvature=False):
        self.reposition(*get_position_vectors(trajectory, prop, use_curvature=use_curvature))

    def set_partial(self, a, b):
        # Eh, no good
        opacities = self.data["opacity"].flatten()
        low_index = int(a * len(opacities))
        high_index = int(b * len(opacities))
        opacities[:] = 1
        opacities[:low_index] = 0
        opacities[high_index:] = 0
        self.set_opacity(opacities)
        return self


class OrientAModel(InteractiveScene):
    def construct(self):
        # Add coordinate system
        frame = self.frame
        frame.reorient(11, 74, 0)
        axes = ThreeDAxes((-4, 4), (-4, 4), (-4, 4))
        axes.set_stroke(GREY_B, 1)
        xy_plane = NumberPlane((-4, 4), (-4, 4))
        xy_plane.axes.set_stroke(width=0)
        xy_plane.background_lines.set_stroke(GREY, 1, 0.5)
        xy_plane.faded_lines.set_stroke(GREY, 0.5, 0.25)

        frame.reorient(34, 76, 0, (-0.16, 0.01, 0.38), 8.16)

        # Add the plane
        plane = S3Viking(height=0.5)
        plane.scale(4, about_point=ORIGIN)

        frame.reorient(11, 49, 0)
        self.play(
            GrowFromPoint(plane, ORIGIN, time_span=(0, 2)),
            frame.animate.reorient(-33, 79, 0, (-0.16, 0.01, 0.38), 8.16),
            run_time=4
        )
        frame.add_ambient_rotation(1 * DEG)

        # Helix trajectory
        traj1 = ParametricCurve(
            lambda t: 2 * np.array([math.cos(t), math.sin(t), 0.04 * t**1.5 - 1]),
            t_range=(0, 15, 0.2)
        )
        traj1.set_stroke(YELLOW, 3, 0.5)
        traj1.set_z_index(1)
        prop_tracker = ValueTracker(0)

        def update_plane(s3, use_curvature=False):
            s3.place_on_path(traj1, prop_tracker.get_value(), use_curvature=use_curvature)

        self.play(
            plane.animate.place_on_path(traj1, prop_tracker.get_value()),
            ShowCreation(traj1),
            FadeIn(axes),
            FadeIn(xy_plane),
        )
        self.play(
            prop_tracker.animate.set_value(1),
            UpdateFromFunc(plane, update_plane),
            rate_func=linear,
            run_time=10
        )

        # Tweaked Gaussian trajectory
        traj2 = ParametricCurve(
            lambda t: t * RIGHT + np.exp(-0.1 * t**2) * (math.cos(2 * t) * UP + math.sin(2 * t) * OUT) + 2 * OUT,
            t_range=(-4, 4, 0.1)
        )
        traj2.match_style(traj1)
        prop_tracker.set_value(0)

        self.play(
            plane.animate.place_on_path(traj2, 0),
            Transform(traj1, traj2),
            run_time=2
        )
        self.play(
            prop_tracker.animate.set_value(1),
            UpdateFromFunc(plane, update_plane),
            frame.animate.reorient(41, 64, 0, (-0.17, 0.0, 0.38), 8.16),
            rate_func=linear,
            run_time=10
        )

        # Show a given point
        prop_tracker.set_value(0.2)
        traj1.insert_n_curves(1000)
        pre_traj = traj1.copy().pointwise_become_partial(traj1, 0, prop_tracker.get_value())
        pre_traj.set_stroke(WHITE, 0.75)
        plane.always_sort_to_camera(self.camera)

        vel_vector, wing_vector, center_dot = vect_group = Group(
            Vector(RIGHT, thickness=2).set_color(RED),
            Vector(RIGHT, thickness=2).set_color(PINK),
            TrueDot(radius=0.025, color=BLUE).make_3d(),
        )
        vect_group.set_z_index(2)
        vect_group.deactivate_depth_test()

        def update_vect_group(vect_group, use_curvature=False):
            center, vel, wing_dir = get_position_vectors(traj1, prop_tracker.get_value(), use_curvature=use_curvature)
            heading, wing, dot = vect_group
            dot.move_to(center)
            heading.put_start_and_end_on(center, center + vel)
            wing.put_start_and_end_on(center, center + wing_dir)

        update_vect_group(vect_group)
        vel_vector.always.set_perpendicular_to_camera(frame)
        wing_vector.always.set_perpendicular_to_camera(frame)

        self.add(pre_traj)
        self.play(
            plane.animate.reposition(center_dot.get_center(), RIGHT, UP).set_opacity(0.5),
            frame.animate.reorient(-7, 66, 0, (-1.99, -0.11, 1.79), 3.67),
            traj1.animate.set_stroke(GREY, 1, 0.5),
            FadeIn(center_dot),
            run_time=3
        )
        self.wait()
        self.play(Rotate(plane, TAU, axis=UR + OUT, about_point=center_dot.get_center()), run_time=6)
        self.wait()
        self.add(vel_vector, center_dot)
        self.play(GrowArrow(vel_vector))
        self.play(plane.animate.place_on_path(traj1, prop_tracker.get_value()), run_time=2)
        self.wait()
        self.play(Rotate(plane, TAU, axis=vel_vector.get_vector(), about_point=center_dot.get_center(), run_time=5))
        self.wait()
        self.play(GrowArrow(wing_vector))
        self.wait()
        self.play(
            Rotate(plane, TAU, axis=vel_vector.get_vector(), about_point=center_dot.get_center(), run_time=5),
            Rotate(wing_vector, TAU, axis=vel_vector.get_vector(), about_point=center_dot.get_center(), run_time=5),
        )
        self.wait()

        # Continue on the trajectory
        self.play(traj1.animate.set_stroke(WHITE, 1), FadeOut(pre_traj))
        self.play(
            UpdateFromFunc(plane, update_plane),
            UpdateFromFunc(vect_group, update_vect_group),
            prop_tracker.animate.set_value(1).set_anim_args(rate_func=linear),
            frame.animate.reorient(27, 69, 0, (-0.05, -0.3, 0.71), 8.18),
            run_time=10,
        )

        # One more trajectory
        traj3 = ParametricCurve(
            lambda t: 3 * math.cos(t) * RIGHT + 3 * math.sin(t) * UP + math.cos(3 * t) * OUT,
            t_range=(0, TAU, 0.01),
        )
        traj3.insert_n_curves(1000)
        traj3.set_stroke(WHITE, 1)
        center, vel, wing_dir = get_position_vectors(traj3, 0, use_curvature=False)

        prop_tracker.set_value(0)
        self.play(
            traj1.animate.become(traj3),
            plane.animate.place_on_path(traj3, 0).set_opacity(1),
            center_dot.animate.move_to(center),
            vel_vector.animate.put_start_and_end_on(center, center + vel),
            wing_vector.animate.put_start_and_end_on(center, center + wing_dir),
            frame.animate.reorient(-3, 47, 0, (-0.36, -0.81, -0.05), 8.18),
            run_time=2
        )
        self.play(
            UpdateFromFunc(plane, update_plane),
            UpdateFromFunc(vect_group, update_vect_group),
            prop_tracker.animate.set_value(1).set_anim_args(rate_func=linear),
            frame.animate.reorient(-49, 71, 0, (0.47, 0.37, 0.28), 6.45),
            run_time=10,
        )
        prop_tracker.set_value(0)
        self.play(
            prop_tracker.animate.set_value(1).set_anim_args(rate_func=linear),
            UpdateFromFunc(plane, update_plane),
            UpdateFromFunc(vect_group, update_vect_group),
            run_time=10
        )

        # Put plane in the center
        v_tracker = Point(normalize(vel_vector.get_vector()))
        self.play(
            plane.animate.reposition(ORIGIN, v_tracker.get_center(), faulty_perp(v_tracker.get_center())).set_opacity(0.3),
            center_dot.animate.move_to(ORIGIN),
            vel_vector.animate.put_start_and_end_on(ORIGIN, v_tracker.get_center()),
            wing_vector.animate.put_start_and_end_on(ORIGIN, faulty_perp(v_tracker.get_center())),
            FadeOut(traj1),
            frame.animate.reorient(-42, 74, 0, (-0.14, 0.44, -0.03), 3.68),
            run_time=5
        )

        # Add sphere of headings
        axis_tracker = Point(RIGHT)
        rot_group = Group(plane, vel_vector, wing_vector)
        wing_rotation = ValueTracker(0)
        wing_vector_offset = ValueTracker(0)

        sphere = Sphere(radius=1)
        sphere.set_color(GREY, 0.1)
        sphere.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(sphere, resolution=(51, 26))
        mesh.set_stroke(WHITE, 2, 0.1)

        path = TracingTail(vel_vector.get_end, time_traced=10, stroke_color=RED)

        def update_v_tracker(v_tracker, dt):
            axis_tracker.rotate(dt * 10 * DEG, axis=DOWN, about_point=ORIGIN)
            v_tracker.rotate(dt * 31 * DEG, axis=axis_tracker.get_center(), about_point=ORIGIN)
            v_tracker.move_to(normalize(v_tracker.get_center()))

        def update_rot_group(group, dt):
            plane, vel_vector, wing_vector = group
            heading = v_tracker.get_center()
            wing_vect = rotate_vector(faulty_perp(heading), wing_rotation.get_value(), axis=heading)
            plane.reposition(ORIGIN, heading, wing_vect)
            vel_vector.put_start_and_end_on(ORIGIN, heading)
            wing_vector.put_start_and_end_on(ORIGIN, wing_vect)
            wing_vector.shift(wing_vector_offset.get_value() * heading)
            vel_vector.set_perpendicular_to_camera(frame)
            wing_vector.set_perpendicular_to_camera(frame)

        v_tracker.add_updater(update_v_tracker)
        rot_group.add_updater(update_rot_group)
        frame.add_ambient_rotation(2 * DEG)
        self.add(v_tracker, rot_group, path)
        self.wait(5)
        self.add(rot_group, mesh, sphere)
        self.play(ShowCreation(sphere), Write(mesh))
        self.wait(15)
        wing_rotation.set_value(90 * DEG)
        self.wait(4)
        wing_rotation.set_value(0)
        self.wait(6)
        self.play(VFadeOut(path))

        # Note infinitley many choices
        v_tracker.suspend_updating()
        frame.clear_updaters()
        self.play(v_tracker.animate.move_to(UP))

        wing_path = TracedPath(wing_vector.get_end, stroke_color=PINK)

        self.add(wing_path)
        wing_rotation.set_value(0)
        self.play(
            wing_rotation.animate.set_value(TAU).set_anim_args(run_time=6),
            frame.animate.reorient(135, 75, 0, (-0.14, 0.44, -0.03), 3.68).set_anim_args(run_time=10),
        )
        wing_path.clear_updaters()

        # Rotate heading around
        self.play(
            Rotate(
                Group(v_tracker, wing_path),
                TAU,
                axis=UR,
                about_point=ORIGIN,
            ),
            run_time=10
        )
        self.wait()

        # Note that wing vector is tangent
        tangent_plane = Square()
        tangent_plane.center()
        tangent_plane.set_width(2.5)
        tangent_plane.set_fill(WHITE, 0.15)
        tangent_plane.set_stroke(WHITE, 0.0)
        tangent_plane.save_state()
        wing_vector_offset.set_value(0)

        def update_tangent_plane(tangent_plane):
            tangent_plane.restore()
            tangent_plane.apply_matrix(rotation_between_vectors(OUT, v_tracker.get_center()))
            tangent_plane.shift(wing_vector_offset.get_value() * v_tracker.get_center())

        update_tangent_plane(tangent_plane)
        tangent_plane.set_opacity(0)

        self.add(tangent_plane, sphere, mesh)
        self.play(
            tangent_plane.animate.shift(1.01 * v_tracker.get_center()).set_fill(opacity=0.15),
            wing_path.animate.shift(1.01 * v_tracker.get_center()),
            wing_vector_offset.animate.set_value(1),
            run_time=2
        )
        self.play(
            frame.animate.reorient(73, 72, 0, (-0.14, 0.44, -0.03), 3.68),
            wing_rotation.animate.set_value(0),
            run_time=6
        )

        # Show the full vector field
        frame.clear_updaters()
        frame.add_ambient_rotation(-2 * DEG)

        points = fibonacci_sphere(1000)

        field = VectorField(
            lambda ps: np.array([faulty_perp(p) for p in ps]),
            axes,
            sample_coords=1.01 * points,
            color=PINK,
            max_vect_len_to_step_size=2,
            density=1,
            tip_width_ratio=4,
            tip_len_to_width=0.005,
        )
        field.set_stroke(opacity=0.8)
        field.apply_depth_test()
        field.add_updater(lambda m: m.update_vectors())
        field.set_stroke(PINK, opacity=0.5)

        tangent_plane.add_updater(update_tangent_plane)
        self.add(tangent_plane)
        self.play(FadeOut(wing_path))
        v_tracker.resume_updating()
        self.play(FadeIn(field, run_time=3))
        self.wait(10)
        tangent_plane.clear_updaters()
        self.play(FadeOut(tangent_plane))

        # Show the glitch
        v_tracker.suspend_updating()
        frame.clear_updaters()
        self.play(
            frame.animate.reorient(-22, 41, 0, (-0.1, -0.02, 0.13), 2.89),
            v_tracker.animate.move_to(normalize(LEFT + OUT)),
            plane.animate.set_opacity(0.5),
            run_time=2
        )
        self.play(
            Rotate(v_tracker, TAU, axis=UP, about_point=ORIGIN),
            run_time=10,
        )

    def alternate_trajectories(self):
        # Vertical loop
        traj1 = ParametricCurve(
            lambda t: 2 * np.array([math.sin(t), 0, -math.cos(t)]),
            t_range=(0, TAU, 0.1)
        )
        traj1.set_stroke(YELLOW, 3, 0.5)
        traj1.set_z_index(1)
        prop_tracker = ValueTracker(0)

        def update_plane(s3, use_curvature=False):
            s3.place_on_path(traj1, prop_tracker.get_value(), use_curvature=use_curvature)

        self.play(
            plane.animate.place_on_path(traj1, prop_tracker.get_value()),
            ShowCreation(traj1),
            FadeIn(axes),
            FadeIn(xy_plane),
            frame.animate.reorient(-52, 71, 0, (-0.29, 0.06, 0.48), 5.98),
        )
        self.play(
            prop_tracker.animate.set_value(1),
            UpdateFromFunc(plane, update_plane),
            rate_func=linear,
            run_time=8
        )
