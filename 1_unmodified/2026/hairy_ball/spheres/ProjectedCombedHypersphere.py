# ==============================================================================
# Scene:      ProjectedCombedHypersphere
# Source:     videos/_2026/hairy_ball/spheres.py (lines 2126-2193)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProjectedCombedHypersphere.py ProjectedCombedHypersphere -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import numpy as np

class ProjectedCombedHypersphere(InteractiveScene):
    def construct(self):
        # Set up
        frame = self.frame
        axes = ThreeDAxes((-5, 5), (-5, 5), (-5, 5))
        plane = NumberPlane((-5, 5), (-5, 5))
        plane.background_lines.set_stroke(BLUE, 1)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.5)
        frame.reorient(86, 78, 0, (-0.13, 0.04, 0.63))
        self.add(axes)

        # Add lines
        flow_lines = VGroup(
            self.get_flow_line_from_point(normalize(np.random.normal(0, 1, 4)))
            for n in range(2000)
        )
        for line in flow_lines:
            line.virtual_time = TAU
            line.get_center()
            stroke_width = clip(get_norm(line.get_center()), 0, 3)
            color = random_bright_color(hue_range=(0.45, 0.55))
            line.set_stroke(color, stroke_width)

        self.add(flow_lines)

        frame.add_ambient_rotation(4 * DEG)
        self.play(
            LaggedStartMap(
                VShowPassingFlash,
                flow_lines,
                lag_ratio=3 / len(flow_lines),
                run_time=45,
                time_width=0.7,
                rate_func=linear
            )
        )

    def get_flow_line_from_point(self, point4d, stroke_color=WHITE, stroke_width=2):
        points4d = self.get_hypersphere_circle_points(point4d)
        points3d = self.streo_4d_to_3d(points4d)
        line = VMobject().set_points_smoothly(points3d)
        line.set_stroke(stroke_color, stroke_width)
        return line

    def get_hypersphere_circle_points(self, point4d, n_samples=100):
        x, y, z, w = point4d
        perp = np.array([-y, x, -w, z])
        return np.array([
            math.cos(a) * point4d + math.sin(a) * perp
            for a in np.linspace(0, TAU, n_samples)
        ])

    def streo_4d_to_3d(self, points4d):
        xyz = points4d[:, :3]
        w = points4d[:, 3]

        # Stereographic projection formula: (x, y, z) / (1 - w)
        # Reshape w for broadcasting
        denominator = (1 - w).reshape(-1, 1)

        # Handle potential division by zero (north pole)
        # Add small epsilon to avoid exact division by zero
        epsilon = 1e-10
        denominator = np.where(np.abs(denominator) < epsilon, epsilon, denominator)

        projected = xyz / denominator

        return projected
