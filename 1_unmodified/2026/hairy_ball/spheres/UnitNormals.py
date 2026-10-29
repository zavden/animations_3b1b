# ==============================================================================
# Scene:      UnitNormals
# Source:     videos/_2026/hairy_ball/spheres.py (lines 1355-1395)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnitNormals.py UnitNormals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import numpy as np

class UnitNormals(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        surface = Torus()
        surface.set_color(GREY_D)

        uv_samples = np.array([
            [u, v]
            for v in np.linspace(0, TAU, 25)
            for u in np.linspace(0, TAU, 50)
        ])
        points = np.array([surface.uv_to_point(u, v) for u, v in uv_samples])
        uv_samples = uv_samples[np.argsort(points[:, 0])]

        normal_vectors = VGroup(
            VMobject().set_points_as_corners([ORIGIN, RIGHT, RIGHT, 2 * RIGHT])
            for sample in uv_samples
        )
        for vect in normal_vectors:
            vect.set_stroke(BLUE_D, width=[2, 2, 2, 12, 6, 0], opacity=0.5)
        normal_vectors.set_stroke(WHITE)
        normal_vectors.apply_depth_test()
        normal_vectors.set_flat_stroke(False)

        def update_normal_vectors(normal_vectors):
            points = np.array([surface.uv_to_point(u, v) for u, v in uv_samples])
            du_points = np.array([surface.uv_to_point(u + 0.1, v) for u, v in uv_samples])
            dv_points = np.array([surface.uv_to_point(u, v + 0.1) for u, v in uv_samples])
            normals = normalize_along_axis(np.cross(du_points - points, dv_points - points), 1)
            for point, normal, vector in zip(points, normals, normal_vectors):
                vector.put_start_and_end_on(point, point + 0.5 * normal)

        update_normal_vectors(normal_vectors)

        frame.reorient(51, 57, 0, (0.39, 0.01, -0.5), 8.00)
        frame.add_ambient_rotation(5 * DEG)
        self.add(surface)
        self.add(normal_vectors)
        self.play(ShowCreation(normal_vectors, run_time=3))
        self.wait(6)
