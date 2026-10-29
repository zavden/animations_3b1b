# ==============================================================================
# Scene:      ThreeSpinExamples
# Source:     videos/_2021/quick_eigen.py (lines 2299-2332)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeSpinExamples.py ThreeSpinExamples -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeSpinExamples(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.focal_distance = 20
        frame.reorient(-20, 70)

        axes = ThreeDAxes(
            (-1, 1), (-1, 1), (-1, 1),
            axis_config={"tick_size": 0, "include_tip": False}
        )
        axes.insert_n_curves(10)
        axes.flat_stroke = False
        axes.set_stroke(WHITE, 3)
        axes.apply_depth_test()

        all_axes = axes.get_grid(3, 1)
        all_axes.arrange(IN, buff=0.8)
        self.add(all_axes)

        for axes, vect, color in zip(all_axes, [RIGHT, UP, OUT], [RED, GREEN, BLUE]):
            sphere = Sphere()
            sphere.scale(0.9)
            mesh = SurfaceMesh(sphere, resolution=(21, 11))
            mesh.set_stroke(color, width=1, opacity=0.8)
            mesh.apply_matrix(z_to_vector(vect))
            sphere = Group(sphere, mesh)
            sphere.scale(0.5)
            sphere.move_to(axes)
            axes.sphere = sphere
            sphere.vect = vect
            sphere.add_updater(lambda m, dt: m.rotate(dt, m.vect))
            self.add(sphere)

        self.wait(2 * TAU)
