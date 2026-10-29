# ==============================================================================
# Scene:      FourierCoefficients
# Source:     videos/_2022/convolutions/discrete.py (lines 2762-2804)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FourierCoefficients.py FourierCoefficients -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed the line "equations = VGroup" (uninstantiated class, half-finished scene in the original) that overwrote the equations
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

# TODO
class FourierCoefficients(InteractiveScene):
    def construct(self):
        # Axes
        axes = Axes((0, 1, 0.1), (0, 2), width=8, height=4)
        axes.add_coordinate_labels(font_size=24, num_decimal_places=1)
        axes.to_edge(DOWN)
        self.add(axes)

        def f(x):
            return max(np.exp(-x**2) + math.cos(2 * PI * x) - 0.2 * math.sin(4 * PI * x), 0.25)

        graph = axes.get_graph(f)
        graph.set_stroke(BLUE, 2)

        self.add(graph)

        # Coefficients
        exp = R"{\left(e^{2\pi i \cdot t}\right)}"
        kw = dict(tex_to_color_map={
            "{x}": BLUE,
            exp: TEAL,
        })
        equations = VGroup(
            Tex(R"f(x) = c_0 + c_1 {x} + c_2 {x}^2 + c_3 {x}^3 + \dots", **kw),
            Tex(Rf"f(t) = c_0 + c_1 {exp} + c_2 {exp}^2 + c_3 {exp}^3 + \dots", **kw),
            Tex(Rf"f(t) = \cdots + c_{{-1}} {exp}^{{-1}} + c_0 + c_1 {exp} + c_2 {exp}^2 + \dots", **kw),
            # Tex(R"f(t) = \cdots + \hat f(-1) e^{-2\pi i t} + \hat f(0) + \hat f(1) e^{2\pi i t} + \hat f(2) e^{2\pi i \cdot 2t} + \dots"),
        )

        # CHANGE: the original line "equations = VGroup" (without parentheses, half-finished "TODO" scene) overwrote the list of equations with the class
        last = VMobject()
        last.move_to(FRAME_HEIGHT * UP / 2)
        for equation in equations:
            equation.next_to(last, DOWN, MED_LARGE_BUFF)
            self.play(FadeIn(equation, DOWN))
            self.wait()
            self.play(
                FadeOut(last, UP),
                equation.animate.to_edge(UP)
            )
            last = equation
