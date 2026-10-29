# ==============================================================================
# Scene:      DataPointsToPolynomial
# Source:     videos/_2022/convolutions/discrete.py (lines 2133-2189)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DataPointsToPolynomial.py DataPointsToPolynomial -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def prod(values):
    return reduce(op.mul, values, 1)


def get_lagrange_polynomial(data):
    def poly(x):
        return sum(
            y0 * prod(
                (x - x1) for x1, y1 in data if x1 != x0
            ) / prod(
                (x0 - x1) for x1, y1 in data if x1 != x0
            )
            for x0, y0 in data
        )

    return poly


class DataPointsToPolynomial(InteractiveScene):
    def construct(self):
        # Axes
        axes = Axes((-1, 10), (-3, 3), width=FRAME_WIDTH - 2, height=4)
        kw = dict(font_size=30)
        axes.add(OldTex("x", **kw).next_to(axes.x_axis.get_end(), DR, buff=0.2))
        axes.add(OldTex("y", **kw).next_to(axes.y_axis.get_end(), LEFT, MED_SMALL_BUFF))

        self.add(axes)

        # Graphs and data points
        y_values = [3, 1, 2, -3, -1, 2, 0, 0, 1]
        data = list(enumerate(y_values))
        dots = Group(*(
            GlowDot(axes.c2p(x, y), glow_factor=0.8, radius=0.1)
            for x, y in data
        ))
        dots.set_color(TEAL)
        circles = VGroup(*(
            Circle(radius=0.075).set_stroke(YELLOW, 2).move_to(dot)
            for dot in dots
        ))

        graphs = VGroup(*(
            axes.get_graph(get_lagrange_polynomial(data[:n]))
            for n in range(1, len(data) + 1)
        ))
        graphs.set_stroke(BLUE, 2)

        # Increasing polynomials
        poly_tex = OldTex(
            "a_0", "+", "a_1 x", "+", *it.chain(*(
                (f"a_{n} x^{n}", "+")
                for n in range(2, len(data) - 1)
            ))
        )
        poly_tex.to_corner(UR)

        graph = graphs[1].copy()
        self.play(
            LaggedStartMap(FadeIn, dots[:2], lag_ratio=0.7, run_time=1),
            LaggedStartMap(ShowCreationThenFadeOut, circles[:2], lag_ratio=0.2, run_time=1),
        )
        self.play(
            ShowCreation(graph),
            FadeIn(poly_tex[:3])
        )
        self.wait()
        for n in range(2, len(data) - 1):
            self.play(
                ShowCreationThenFadeOut(circles[n], run_time=1.5),
                FadeIn(dots[n]),
                Transform(graph, graphs[n]),
                FadeIn(poly_tex[2 * n - 1:2 * n + 1], time_span=(0, 1), lag_ratio=0.1),
                run_time=2
            )
            self.wait()
