# ==============================================================================
# Scene:      ExampleApproximationWithExp
# Source:     videos/_2017/eoc/chapter10.py (lines 143-161)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExampleApproximationWithExp.py ExampleApproximationWithExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def derivative(func, x, n = 1, dx = 0.01):
    samples = [func(x + (k - n/2)*dx) for k in range(n+1)]
    while len(samples) > 1:
        samples = [
            (s_plus_dx - s)/dx
            for s, s_plus_dx in zip(samples, samples[1:])
        ]
    return samples[0]


def taylor_approximation(func, highest_term, center_point = 0):
    derivatives = [
        derivative(func, center_point, n = n)
        for n in range(highest_term + 1)
    ]
    coefficients = [
        d/math.factorial(n) 
        for n, d in enumerate(derivatives)
    ]
    return lambda x : sum([
        c*((x-center_point)**n) 
        for n, c in enumerate(coefficients)
    ])


class ExampleApproximation(GraphScene):
    CONFIG = {
        "function" : lambda x : np.exp(-x**2),
        "function_tex" : "e^{-x^2}", 
        "function_color" : BLUE,
        "order_sequence" : [0, 2, 4],
        "center_point" : 0,
        "approximation_terms" : ["1 ", "-x^2", "+\\frac{1}{2}x^4"],
        "approximation_color" : GREEN,
        "x_min" : -3,
        "x_max" : 3,
        "y_min" : -1,
        "y_max" : 2,
        "graph_origin" : DOWN + 2*LEFT,
    }
    def construct(self):
        self.setup_axes()
        func_graph = self.get_graph(
            self.function,
            self.function_color,
        )
        approx_graphs = [
            self.get_graph(
                taylor_approximation(self.function, n),
                self.approximation_color
            )
            for n in self.order_sequence
        ]

        near_text = OldTexText(
            "Near %s $= %d$"%(
                self.x_axis_label, self.center_point
            )
        )
        near_text.to_corner(UP + RIGHT)
        near_text.add_background_rectangle()
        equation = OldTex(
            self.function_tex, 
            "\\approx",
            *self.approximation_terms
        )
        equation.next_to(near_text, DOWN, MED_LARGE_BUFF)
        equation.to_edge(RIGHT)
        near_text.next_to(equation, UP, MED_LARGE_BUFF)
        equation.set_color_by_tex(
            self.function_tex, self.function_color,
            substring = False
        )
        approx_terms = VGroup(*[
            equation.get_part_by_tex(tex, substring = False)
            for tex in self.approximation_terms
        ])
        approx_terms.set_fill(
            self.approximation_color,
            opacity = 0,
        )
        equation.add_background_rectangle()

        approx_graph = VectorizedPoint(
            self.input_to_graph_point(self.center_point, func_graph)
        )

        self.play(
            ShowCreation(func_graph, run_time = 2),
            Animation(equation),
            Animation(near_text),
        )
        for graph, term in zip(approx_graphs, approx_terms):
            self.play(
                Transform(approx_graph, graph, run_time = 2),
                Animation(equation),
                Animation(near_text),
                term.set_fill, None, 1,
            )
            self.wait()
        self.wait(2)


class ExampleApproximationWithExp(ExampleApproximation):
    CONFIG = {
        "function" : np.exp,
        "function_tex" : "e^x", 
        "order_sequence" : [1, 2, 3, 4],
        "center_point" : 0,
        "approximation_terms" : [
            "1 + x", 
            "+\\frac{1}{2}x^2", 
            "+\\frac{1}{6}x^3",
            "+\\frac{1}{24}x^4",
        ],
        "approximation_color" : GREEN,
        "x_min" : -3,
        "x_max" : 4,
        "y_min" : -1,
        "y_max" : 10,
        "graph_origin" : 2*DOWN + 3*LEFT,
    }
