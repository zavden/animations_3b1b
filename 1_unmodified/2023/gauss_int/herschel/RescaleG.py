# ==============================================================================
# Scene:      RescaleG
# Source:     videos/_2023/gauss_int/herschel.py (lines 319-360)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RescaleG.py RescaleG -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RescaleG(InteractiveScene):
    def construct(self):
        def g(x):
            return 0.5 * math.exp(-x**4 + x**2)

        # Setup
        axes = Axes((-2, 2), (0, 1, 0.25), width=6, height=3)
        axes.x_axis.add_numbers()
        axes.y_axis.add_numbers(num_decimal_places=2, excluding=[0], font_size=16)
        self.add(axes)

        curve = axes.get_graph(g)
        curve.make_smooth()
        curve.set_stroke(BLUE, 3)
        curve.save_state()
        curve.generate_target()
        curve.target.stretch(1 / g(0), 1, about_edge=DOWN)

        label1 = TexText(R"$g(0) \ne 1$", font_size=36)
        label2 = TexText(R"$g(0) = 1$", font_size=36)
        label3 = TexText(R"Later we \\ re-scale anyway", font_size=36)
        labels = [label1, label2, label3]
        curves = [curve, curve.target, curve]
        for label, crv in zip(labels, curves):
            label.next_to(crv.get_top(), UR)

        self.play(
            ShowCreation(curve),
            FadeIn(label1, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            MoveToTarget(curve),
            FadeTransform(label1, label2),
        )
        self.wait(2)
        self.play(
            Restore(curve),
            FadeTransform(label2, label3),
        )
        self.play(curve.animate.set_fill(BLUE, 0.5))
        self.wait()
