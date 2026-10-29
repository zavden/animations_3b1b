# ==============================================================================
# Scene:      QuaternionNameAnimation
# Source:     videos/outside_videos/name_animation.py (lines 352-441)
# Category:   3 · Does not render
#
# Run from this folder:
#     manimgl QuaternionNameAnimation.py QuaternionNameAnimation -w -m --fps 15
#
# Why it does not render:
#   Broken in the original: construct uses self.name_text and self.get_axes(), which are never defined (the class inherits plain Scene, not a 3D scene, yet it moves the camera), so it fails with AttributeError in Cairo too.
# ==============================================================================

from manim_imports_ext import *

class QuaternionNameAnimation(Scene):
    CONFIG = {
        "R": 2,
    }

    def construct(self):
        surface = ParametricSurface(lambda u, v: (u, v, 0), resolution=16)
        surface.set_width(self.R * TAU)
        surface.set_height(1.8 * self.R, stretch=True)
        surface.center()
        surface.set_fill(opacity=0.5)
        name = OldTexText(self.name_text)
        name.set_width(self.R * TAU - 1)
        max_height = 0.4 * surface.get_height()
        if name.get_height() > max_height:
            name.set_height(max_height)
        name.next_to(surface.get_top(), DOWN)
        for letter in name:
            letter.add(VectorizedPoint(letter.get_center() + 2 * OUT))
            letter.set_shade_in_3d(True, z_index_as_group=True)
            # for submob in letter.family_members_with_points():
            #     submob.pre_function_handle_to_anchor_scale_factor = 0.001

        axes = self.get_axes()

        self.play(
            Write(surface),
            Write(name),
        )
        surface.add(name)
        self.wait()
        self.move_camera(
            phi=70 * DEGREES,
            theta=-140 * DEGREES,
            added_anims=[
                ApplyPointwiseFunction(self.plane_to_cylinder, surface),
                FadeIn(axes),
            ],
            run_time=3,
        )
        self.begin_ambient_camera_rotation(0.01)
        self.wait(2)
        self.play(
            ApplyPointwiseFunction(self.cylinder_to_sphere, surface),
            run_time=3
        )
        # self.play(Rotating(
        #     surface, angle=-TAU, axis=OUT,
        #     about_point=ORIGIN,
        #     run_time=4,
        #     rate_func=smooth
        # ))
        self.wait(2)
        for i in range(3):
            axis = np.zeros(3)
            axis[i] = 1
            self.play(Homotopy(
                self.get_quaternion_homotopy(axis),
                surface,
                run_time=10,
            ))
        self.wait(5)

    def plane_to_cylinder(self, p):
        x, y, z = p
        R = self.R + z
        return np.array([
            R * np.cos(x / self.R - 0),
            R * np.sin(x / self.R - 0),
            1.0 * y,
        ])

    def cylinder_to_sphere(self, p):
        x, y, z = p
        R = self.R
        r = np.sqrt(R**2 - z**2)
        return np.array([
            x * fdiv(r, R),
            y * fdiv(r, R),
            z
        ])

    def get_quaternion_homotopy(self, axis=[1, 0, 0]):
        def result(x, y, z, t):
            alpha = t
            quaternion = np.array([np.cos(TAU * alpha), 0, 0, 0])
            quaternion[1:] = np.sin(TAU * alpha) * np.array(axis)
            new_quat = q_mult(quaternion, [0, x, y, z])
            return new_quat[1:]
        return result
