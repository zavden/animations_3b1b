# ==============================================================================
# Scene:      SimpleRightwardFlow
# Source:     videos/_2026/hairy_ball/spheres.py (lines 745-776)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleRightwardFlow.py SimpleRightwardFlow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import numpy as np

class SimpleRightwardFlow(InteractiveScene):
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

        # Simple flow
        frame.set_height(4)

        xy_field = VectorField(lambda ps: np.array([RIGHT for p in ps]), plane)
        xy_field.set_stroke(BLUE)
        self.add(xy_field)

        proto_stream_lines = VGroup(
            Line([x, y, 0], [x + 1, y, 0]).insert_n_curves(20)
            for x in np.arange(-10, 10, 0.5)
            for y in np.arange(-10, 10, 0.1)
        )
        for line in proto_stream_lines:
            line.virtual_time = 1
        proto_stream_lines.set_stroke(WHITE, 2, 0.8)

        animated_plane_lines = AnimatedStreamLines(proto_stream_lines, rate_multiple=0.2)

        self.add(animated_plane_lines)
        self.wait(30)
