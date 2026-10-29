# ==============================================================================
# Scene:      Introduction
# Source:     videos/_2018/fourier.py (lines 66-106)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Introduction.py Introduction -w -m --fps 15
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


class Introduction(TeacherStudentsScene):
    def construct(self):
        title = OldTexText("Fourier Transform")
        title.scale(1.2)
        title.to_edge(UP, buff = MED_SMALL_BUFF)

        func = lambda t : np.cos(2*TAU*t) + np.cos(3*TAU*t)
        graph = FunctionGraph(func, x_min = 0, x_max = 5)
        graph.stretch(0.25, 1)
        graph.next_to(title, DOWN)
        graph.to_edge(LEFT)
        graph.set_color(BLUE)
        fourier_graph = FunctionGraph(
            get_fourier_transform(func, 0, 5),
            x_min = 0, x_max = 5
        )
        fourier_graph.move_to(graph)
        fourier_graph.to_edge(RIGHT)
        fourier_graph.set_color(RED)
        arrow = Arrow(graph, fourier_graph, color = WHITE)
        self.add(title, graph)

        self.student_thinks(
            "What's that?",
            look_at = title,
            target_mode = "confused",
            index = 1,
        )
        self.play(
            GrowArrow(arrow),
            ReplacementTransform(graph.copy(), fourier_graph)
        )
        self.wait(2)
        self.student_thinks(
            "Pssht, I got this",
            target_mode = "tease",
            index = 2,
            added_anims = [RemovePiCreatureBubble(self.students[1])]
        )
        self.play(self.teacher.change, "hesitant")
        self.wait(2)
