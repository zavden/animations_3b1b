# ==============================================================================
# Scene:      SecondDerivativeGraphically
# Source:     videos/_2017/eoc/footnote.py (lines 63-301)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SecondDerivativeGraphically.py SecondDerivativeGraphically -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SecondDerivativeGraphically(GraphScene):
    CONFIG = {
        "x1" : 0,
        "x2" : 4,
        "x3" : 8,
        "y" : 4,
        "deriv_color" : YELLOW,
        "second_deriv_color" : GREEN,
    }
    def construct(self):
        self.force_skipping()

        self.setup_axes()
        self.draw_f()
        self.show_derivative()
        self.write_second_derivative()
        self.show_curvature()

        self.revert_to_original_skipping_status()
        self.contrast_big_and_small_concavity()

    def draw_f(self):
        def func(x):
            return 0.1*(x-self.x1)*(x-self.x2)*(x-self.x3) + self.y

        graph = self.get_graph(func)
        graph_label = self.get_graph_label(graph, "f(x)")

        self.play(
            ShowCreation(graph, run_time = 2),
            Write(
                graph_label,
                run_time = 2,
                rate_func = squish_rate_func(smooth, 0.5, 1)
            )
        )
        self.wait()

        self.graph = graph
        self.graph_label = graph_label

    def show_derivative(self):
        deriv = OldTex("\\frac{df}{dx}")
        deriv.next_to(self.graph_label, DOWN, MED_LARGE_BUFF)
        deriv.set_color(self.deriv_color)
        ss_group = self.get_secant_slope_group(
            1, self.graph,
            dx = 0.01,
            secant_line_color = self.deriv_color
        )

        self.play(
            Write(deriv),
            *list(map(ShowCreation, ss_group))
        )
        self.animate_secant_slope_group_change(
            ss_group, target_x = self.x3,
            run_time = 5
        )
        self.wait()
        self.animate_secant_slope_group_change(
            ss_group, target_x = self.x2,
            run_time = 3
        )
        self.wait()

        self.ss_group = ss_group
        self.deriv = deriv

    def write_second_derivative(self):
        second_deriv = OldTex("\\frac{d^2 f}{dx^2}")
        second_deriv.next_to(self.deriv, DOWN, MED_LARGE_BUFF)
        second_deriv.set_color(self.second_deriv_color)
        points = [
            self.input_to_graph_point(x, self.graph)
            for x in (self.x2, self.x3)
        ]
        words = OldTexText("Change to \\\\ slope")
        words.next_to(
            center_of_mass(points), UP, 1.5*LARGE_BUFF
        )
        arrows = [
            Arrow(words.get_bottom(), p, color = WHITE)
            for p in points
        ]

        self.play(Write(second_deriv))
        self.wait()
        self.play(
            Write(words),
            ShowCreation(
                arrows[0], 
                rate_func = squish_rate_func(smooth, 0.5, 1)
            ),
            run_time = 2
        )
        self.animate_secant_slope_group_change(
            self.ss_group, target_x = self.x3,
            run_time = 3,
            added_anims = [
                Transform(
                    *arrows, 
                    run_time = 3,
                    path_arc = 0.75*np.pi
                ),
            ]
        )
        self.play(FadeOut(arrows[0]))
        self.animate_secant_slope_group_change(
            self.ss_group, target_x = self.x2,
            run_time = 3,
        )

        self.second_deriv_words = words
        self.second_deriv = second_deriv

    def show_curvature(self):
        positive_curve, negative_curve = [
            self.get_graph(
                self.graph.underlying_function,
                x_min = x_min,
                x_max = x_max,
                color = color,
            ).set_stroke(width = 6)
            for x_min, x_max, color in [
                (self.x2, self.x3, PINK),
                (self.x1, self.x2, RED),
            ]
        ]
        dot = Dot()
        def get_dot_update_func(curve):
            def update_dot(dot):
                dot.move_to(curve.get_points()[-1])
                return dot
            return update_dot

        self.play(
            ShowCreation(positive_curve, run_time = 3),
            UpdateFromFunc(dot, get_dot_update_func(positive_curve))
        )
        self.play(FadeOut(dot))
        self.wait()
        self.animate_secant_slope_group_change(
            self.ss_group, target_x = self.x3,
            run_time = 4,
            added_anims = [Animation(positive_curve)]
        )

        self.play(*list(map(FadeOut, [self.ss_group, positive_curve])))
        self.animate_secant_slope_group_change(
            self.ss_group, target_x = self.x1,
            run_time = 0
        )
        self.play(FadeIn(self.ss_group))
        self.play(
            ShowCreation(negative_curve, run_time = 3),
            UpdateFromFunc(dot, get_dot_update_func(negative_curve))
        )
        self.play(FadeOut(dot))
        self.animate_secant_slope_group_change(
            self.ss_group, target_x = self.x2,
            run_time = 4,
            added_anims = [Animation(negative_curve)]
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [
            self.graph, self.ss_group, 
            negative_curve, self.second_deriv_words
        ])))

    def contrast_big_and_small_concavity(self):
        colors = color_gradient([GREEN, WHITE], 3)
        x0, y0 = 4, 2
        graphs = [
            self.get_graph(func, color = color)
            for color, func in zip(colors, [
                lambda x : 5*(x - x0)**2 + y0,
                lambda x : 0.2*(x - x0)**2 + y0,
                lambda x : (x-x0) + y0,
            ])
        ]
        arg_rhs_list = [
            OldTex("(", str(x0), ")", "=", str(rhs))
            for rhs in (10, 0.4, 0)
        ]
        for graph, arg_rhs in zip(graphs, arg_rhs_list):
            graph.ss_group = self.get_secant_slope_group(
                x0-1, graph, 
                dx = 0.001,
                secant_line_color = YELLOW
            )
            arg_rhs.move_to(self.second_deriv.get_center(), LEFT)
            graph.arg_rhs = arg_rhs
        graph = graphs[0]

        v_line = DashedLine(*[
            self.coords_to_point(x0, 0),
            self.coords_to_point(x0, y0),
        ])
        input_label = OldTex(str(x0))
        input_label.next_to(v_line, DOWN)

        self.play(ShowCreation(graph, run_time = 2))
        self.play(
            Write(input_label),
            ShowCreation(v_line)
        )
        self.play(
            ReplacementTransform(
                input_label.copy(),
                graph.arg_rhs.get_part_by_tex(str(x0))
            ),
            self.second_deriv.next_to, graph.arg_rhs.copy(), LEFT, SMALL_BUFF,
            Write(VGroup(*[
                submob
                for submob in graph.arg_rhs
                if submob is not graph.arg_rhs.get_part_by_tex(str(x0))
            ]))
        )
        self.wait()
        self.play(FadeIn(graph.ss_group))
        self.animate_secant_slope_group_change(
            graph.ss_group, target_x = x0 + 1,
            run_time = 3,
        )
        self.play(FadeOut(graph.ss_group))
        self.wait()
        for new_graph in graphs[1:]:
            self.play(Transform(graph, new_graph))
            self.play(Transform(
                graph.arg_rhs,
                new_graph.arg_rhs,
            ))
            self.play(FadeIn(new_graph.ss_group))
            self.animate_secant_slope_group_change(
                new_graph.ss_group, target_x = x0 + 1,
                run_time = 3,
            )
            self.play(FadeOut(new_graph.ss_group))
