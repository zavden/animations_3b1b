# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2018/fourier.py (lines 4232-4294)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
import scipy.integrate
from manim_imports_ext import *

USE_ALMOST_FOURIER_BY_DEFAULT = True


DEFAULT_COMPLEX_TO_REAL_FUNC = lambda z : z.real


def get_fourier_transform(
    func, t_min, t_max, 
    complex_to_real_func = DEFAULT_COMPLEX_TO_REAL_FUNC,
    use_almost_fourier = USE_ALMOST_FOURIER_BY_DEFAULT,
    **kwargs ##Just eats these
    ):
    scalar = 1./(t_max - t_min) if use_almost_fourier else 1.0
    def fourier_transform(f):
        z = scalar*scipy.integrate.quad(
            lambda t : func(t)*np.exp(complex(0, -TAU*f*t)),
            t_min, t_max
        )[0]
        return complex_to_real_func(z)
    return fourier_transform


class Thumbnail(Scene):
    def construct(self):
        title = OldTexText("Fourier\\\\", "Visualized")
        title.set_color(YELLOW)
        title.set_stroke(RED, 2)
        title.scale(2.5)
        title.add_background_rectangle()

        def func(t):
            return np.cos(2*TAU*t) + np.cos(3*TAU*t) + np.cos(5*t)
        fourier = get_fourier_transform(func, -5, 5)

        graph = FunctionGraph(func, (-5, 5, 0.01))
        graph.set_color(BLUE)
        fourier_graph = FunctionGraph(fourier, (0, 6, 0.01))
        fourier_graph.set_color(YELLOW)
        for g in graph, fourier_graph:
            g.stretch_to_fit_height(2)
            g.stretch_to_fit_width(10)
            g.set_stroke(width=6)

        pol_graphs = VGroup()
        for f in np.linspace(1.98, 2.02, 5):
            pol_graph = ParametricCurve(
                lambda t : complex_to_R3(
                    (2+np.cos(2*TAU*t)+np.cos(3*TAU*t))*np.exp(-complex(0, TAU*f*t))
                ),
                t_range=(-5, 5, 0.01),
            )
            pol_graph.match_color(graph)
            pol_graph.set_height(2)
            pol_graphs.add(pol_graph)
        pol_graphs.arrange(RIGHT, buff=LARGE_BUFF)
        pol_graphs.set_color_by_gradient(BLUE_C, TEAL, GREEN)
        pol_graphs.match_width(graph)
        pol_graphs.set_stroke(width=1)

        parts = VGroup(graph, pol_graphs, fourier_graph)
        parts[1].set_width(parts[0].get_width() - 1)
        parts.arrange(
            DOWN, buff=LARGE_BUFF,
            aligned_edge=RIGHT
        )
        parts.to_edge(RIGHT)
        self.add(parts)

        words = VGroup(OldTexText("Signal"), OldTexText("Winding"), OldTexText("Transform"))
        for word, part in zip(words, parts):
            word.scale(1.5)
            word.next_to(part, LEFT)
            word.to_edge(LEFT, MED_LARGE_BUFF)

        self.add(words)

        rect = SurroundingRectangle(pol_graphs[2])
        rect.set_stroke(RED, 2)
        dot = Dot(fourier_graph.pfp(2 / 6), color=RED)
        dot.set_stroke(BLACK, 3, background=True)
        dot.shift(0.01 * RIGHT)
        line = Line(dot.get_center(), rect.get_corner(DL), buff=0.1)
        line.match_style(rect)

        self.add(dot, line, rect)
