# ==============================================================================
# Scene:      GeneralDirection
# Source:     videos/_2021/quick_eigen.py (lines 2335-2386)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneralDirection.py GeneralDirection -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeneralDirection(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.reorient(-30, 70)
        frame.add_updater(lambda m, dt: m.increment_theta(0.01 * dt))
        self.add(frame)

        axes = ThreeDAxes(
            (-2, 2), (-2, 2), (-4, 4),
            axis_config={'include_tip': False},
            depth=6,
        )
        axes.set_stroke(width=1)
        self.add(axes)

        vect = axes.c2p(2, 2, 2)
        vector = Vector(vect)
        vector.set_fill(YELLOW)

        label = Matrix([["a"], ["b"], ["c"]], v_buff=0.6)
        # label.get_entries().set_submobject_colors_by_gradient(
        #     YELLOW_B, YELLOW_C, YELLOW_D
        # )
        label.get_entries().set_color(YELLOW)
        label.rotate(89 * DEGREES, RIGHT)
        label.next_to(vector.get_end(), RIGHT)

        sphere = Sphere()
        sphere.scale(0.5)
        mesh = SurfaceMesh(sphere, resolution=(21, 11))
        mesh.set_stroke(BLUE, width=0.5, opacity=0.5)
        for mob in sphere, mesh:
            mob.apply_matrix(z_to_vector(vect))
            mob.add_updater(lambda m, dt: m.rotate(0.75 * dt, axis=vect))

        axes.apply_depth_test()
        for sm in axes.get_family():
            sm.insert_n_curves(10)

        self.add(vector, sphere, mesh)
        self.play(
            GrowArrow(vector),
            UpdateFromAlphaFunc(sphere, lambda m, a: m.set_opacity(a)),
            Write(mesh),
        )
        self.play(Write(label))
        self.wait(6)
        self.play(
            vector.animate.scale(0.5, about_point=ORIGIN),
            label.animate.shift(-0.5 * vect)
        )
        self.wait(24)
