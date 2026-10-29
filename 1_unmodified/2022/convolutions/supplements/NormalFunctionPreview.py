# ==============================================================================
# Scene:      NormalFunctionPreview
# Source:     videos/_2022/convolutions/supplements.py (lines 50-88)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NormalFunctionPreview.py NormalFunctionPreview -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class NormalFunctionPreview(InteractiveScene):
    def construct(self):
        # Setup axes
        frame = self.camera.frame
        axes2d = Axes((-2, 2), (-1, 2), width=10, height=6)
        axes3d = ThreeDAxes((-2, 2), (-2, 2), (-1, 2), width=10, height=10, depth=6)
        axes3d.shift(axes2d.get_origin() - axes3d.get_origin())

        curve = axes2d.get_graph(lambda x: math.exp(-x**2))
        curve.set_stroke(BLUE)
        label = OldTex("e^{-x^2}", font_size=60)
        label.next_to(curve.get_top(), UR).shift(RIGHT)
        label3d = OldTex("e^{-x^2 - y^2}", font_size=60)
        label3d.move_to(label, DL)

        VGroup(axes2d, curve, label, label3d).rotate(PI / 2, RIGHT, about_point=axes3d.get_origin())
        frame.reorient(0, 90)

        self.add(axes2d)
        self.play(ShowCreation(curve), Write(label))

        # Show in 3d
        surface = axes3d.get_graph(lambda x, y: math.exp(-x * x - y * y))
        surface.always_sort_to_camera(self.camera)
        surface_mesh = SurfaceMesh(surface)
        surface_mesh.set_stroke(WHITE, 0.5, 0.5)

        self.add(axes3d, surface, curve)
        self.play(
            FadeIn(axes3d),
            frame.animate.reorient(-10, 70).set_anim_args(run_time=2),
            FadeIn(surface, time_span=(1, 2)),
            FadeIn(label3d),
            FadeOut(label),
            Rotate(curve, PI, run_time=3)
        )
        frame.add_updater(lambda m, dt: m.increment_theta(0.02 * dt))
        self.play(Write(surface_mesh))
        self.wait(8)
