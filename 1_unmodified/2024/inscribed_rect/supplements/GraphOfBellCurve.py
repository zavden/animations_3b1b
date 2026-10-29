# ==============================================================================
# Scene:      GraphOfBellCurve
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 289-304)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GraphOfBellCurve.py GraphOfBellCurve -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GraphOfBellCurve(InteractiveScene):
    def construct(self):
        # Test
        axes = ThreeDAxes((-3, 3), (-3, 3), (0, 1))
        axes.set_depth(2, stretch=True)
        surface = axes.get_graph(lambda x, y: np.exp(-x**2 - y**2))
        surface.set_opacity(0.7)
        surface.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(surface, resolution=(21, 21))
        mesh.set_stroke(WHITE, 0.5, 0.5)

        self.frame.reorient(42, 67, 0, (0.42, 0.43, 0.1), 6.03)
        self.frame.add_ambient_rotation(3 * DEG)
        self.add(axes)
        self.add(surface, mesh)
        self.wait(30)
