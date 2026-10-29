# ==============================================================================
# Scene:      ExampleApproximationWithCos
# Source:     videos/_2017/eoc/chapter10.py (lines 476-536)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExampleApproximationWithCos.py ExampleApproximationWithCos -w -m --fps 15
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


class ExampleApproximationWithSine(ExampleApproximation):
    CONFIG = {
        "function" : np.sin,
        "function_tex" : "\\sin(x)", 
        "order_sequence" : [1, 3, 5],
        "center_point" : 0,
        "approximation_terms" : [
            "x", 
            "-\\frac{1}{6}x^3", 
            "+\\frac{1}{120}x^5",
        ],
        "approximation_color" : GREEN,
        "x_min" : -2*np.pi,
        "x_max" : 2*np.pi,
        "x_tick_frequency" : np.pi/2,
        "y_min" : -2,
        "y_max" : 2,
        "graph_origin" : DOWN + 2*LEFT,
    }


class ExampleApproximationWithCos(ExampleApproximationWithSine):
    CONFIG = {
        "function" : np.cos,
        "function_tex" : "\\cos(\\theta)", 
        "order_sequence" : [0, 2],
        "approximation_terms" : [
            "1", 
            "-\\frac{1}{2} \\theta ^2", 
        ],
        "x_axis_label" : "$\\theta$",
        "y_axis_label" : "",
        "x_axis_width" : 13,
        "graph_origin" : DOWN,
    }

    def construct(self):
        ExampleApproximationWithSine.construct(self)
        randy = Randolph(color = BLUE_C)
        randy.to_corner(DOWN+LEFT)
        high_graph = self.get_graph(lambda x : 4)
        v_lines, alt_v_lines = [
            VGroup(*[
                self.get_vertical_line_to_graph(
                    u*dx, high_graph,
                    line_class = DashedLine,
                    color = YELLOW
                )
                for u in (-1, 1)
            ])
            for dx in (0.01, 0.7)
        ]

        self.play(*list(map(ShowCreation, v_lines)), run_time = 2)
        self.play(Transform(
            v_lines, alt_v_lines,
            run_time = 2,
        ))
        self.play(FadeIn(randy))
        self.play(PiCreatureBubbleIntroduction(
            randy, "How...?",
            bubble_type = ThoughtBubble,
            look_at = self.graph_origin,
            target_mode = "confused"
        ))
        self.wait(2)
        self.play(Blink(randy))
        self.wait()

    def setup_axes(self):
        GraphScene.setup_axes(self)
        x_val_label_pairs = [
            (-np.pi, "-\\pi"),
            (np.pi, "\\pi"),
            (2*np.pi, "2\\pi"),
        ]
        self.x_axis_labels = VGroup()
        for x_val, label in x_val_label_pairs:
            tex = OldTex(label)
            tex.next_to(self.coords_to_point(x_val, 0), DOWN)
            self.add(tex)
            self.x_axis_labels.add(tex)
