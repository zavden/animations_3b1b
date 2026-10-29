# ==============================================================================
# Scene:      ManyDifferentFs
# Source:     videos/_2023/gauss_int/herschel.py (lines 363-403)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyDifferentFs.py ManyDifferentFs -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ManyDifferentFs(InteractiveScene):
    def construct(self):
        axes = Axes((0, 4), (0, 1, 0.25), width=6, height=3)
        axes.x_axis.add_numbers()
        axes.y_axis.add_numbers(num_decimal_places=2, excluding=[0], font_size=16)
        self.add(axes)

        # Many curves
        curves = VGroup(
            axes.get_graph(lambda x: math.exp(-x**2)),
            axes.get_graph(lambda x: 1 / (1 + x**2)),
            axes.get_graph(lambda x: math.exp(-x)),
            axes.get_graph(lambda x: 0.5 * math.exp(-x**4 + x**2)),
            axes.get_graph(lambda x: math.cos(x)**2 / (x + 1)),
            axes.get_graph(lambda x: (1 / 2) * (x**2) * np.exp(-x)),
        )
        curves.set_stroke(RED, 3)
        func_names = VGroup(
            Tex("e^{-x^2}"),
            Tex(R"1 \over (1 + x^2)"),
            Tex("e^{-x}"),
            Tex(R"\frac{1}{2} e^{-x^4 + x^2}"),
            Tex(R"\cos^2(x) \over (x + 1)"),
            Tex(R"\frac{1}{2} x^2 e^{-x}"),
        )
        func_names.move_to(axes.get_top())

        curve = curves[0]
        name = func_names[0]
        self.play(
            ShowCreation(curve),
            FadeIn(name, 0.5 * UP)
        )
        self.wait()
        for new_curve, new_name in zip(curves[1:], func_names[1:]):
            self.play(
                Transform(curve, new_curve),
                TransformMatchingTex(name, new_name, run_time=1)
            )
            name = new_name
            self.wait()
