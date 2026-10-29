# ==============================================================================
# Scene:      FundamentalTheorem
# Source:     videos/_2017/eoc/chapter8.py (lines 2257-2464)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/eoc/chapter1.py
#
# Run from this folder:
#     manimgl FundamentalTheorem.py FundamentalTheorem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter1.py -----

class FundamentalTheorem(Scene):
    def construct(self):
        words = OldTexText("""
            Fundamental theorem of calculus
        """)
        words.to_edge(UP)
        arrow = DoubleArrow(LEFT, RIGHT).shift(2*RIGHT)
        deriv = OldTex(
            "{dA", "\\over \\,", "dx}", "=", "x^2"
        )
        deriv.set_color_by_tex("dA", GREEN)
        deriv.next_to(arrow, RIGHT)

        self.play(ShowCreation(arrow))
        self.wait()
        self.play(Write(deriv))
        self.wait()
        self.play(Write(words))
        self.wait()



# ----- From _2017/eoc/chapter8.py -----

class FundamentalTheorem(GraphScene):
    CONFIG = {
        "lower_bound" : 1,
        "upper_bound" : 7,
        "lower_bound_color" : RED,
        "upper_bound_color" : GREEN,
        "n_riemann_iterations" : 6,
    }

    def construct(self):
        self.add_graph_and_integral()
        self.show_f_dx_sum()
        self.show_rects_approaching_area()
        self.write_antiderivative()
        self.write_fundamental_theorem_of_calculus()
        self.show_integral_considering_continuum()
        self.show_antiderivative_considering_bounds()

    def add_graph_and_integral(self):
        self.setup_axes()
        integral = OldTex("\\int", "^b", "_a", "f(x)", "\\,dx")
        integral.next_to(ORIGIN, LEFT)
        integral.to_edge(UP)
        integral.set_color_by_tex("a", self.lower_bound_color)
        integral.set_color_by_tex("b", self.upper_bound_color)
        graph = self.get_graph(
            lambda x : -0.01*x*(x-3)*(x-6)*(x-12) + 3,
        )
        self.add(integral, graph)
        self.graph = graph
        self.integral = integral

        self.bound_labels = VGroup()
        self.v_lines = VGroup()
        for bound, tex in (self.lower_bound, "a"), (self.upper_bound, "b"):
            label = integral.get_part_by_tex(tex).copy()
            label.scale(1.5)
            label.next_to(self.coords_to_point(bound, 0), DOWN)
            v_line = self.get_vertical_line_to_graph(
                bound, graph, color = label.get_color()
            )

            self.bound_labels.add(label)
            self.v_lines.add(v_line)
            self.add(label, v_line)

    def show_f_dx_sum(self):
        kwargs = {
            "x_min" : self.lower_bound,
            "x_max" : self.upper_bound,
            "fill_opacity" : 0.75,
            "stroke_width" : 0.25,
        }
        low_opacity = 0.25
        start_rect_index = 3
        num_shown_sum_steps = 5
        last_rect_index = start_rect_index + num_shown_sum_steps + 1

        self.rect_list = self.get_riemann_rectangles_list(
            self.graph, self.n_riemann_iterations, **kwargs
        )
        rects = self.rects = self.rect_list[0]
        rects.save_state()

        start_rect = rects[start_rect_index]
        f_brace = Brace(start_rect, LEFT, buff = 0)
        dx_brace = Brace(start_rect, DOWN, buff = 0)
        f_brace.label = f_brace.get_text("$f(x)$")
        dx_brace.label = dx_brace.get_text("$dx$")

        flat_rects = self.get_riemann_rectangles(
            self.get_graph(lambda x : 0), dx = 0.5, **kwargs
        )

        self.transform_between_riemann_rects(
            flat_rects, rects, 
            replace_mobject_with_target_in_scene = True,
        )
        self.play(*[
            ApplyMethod(
                rect.set_fill, None, 
                1 if rect is start_rect else low_opacity
            )
            for rect in rects
        ])
        self.play(*it.chain(
            list(map(GrowFromCenter, [f_brace, dx_brace])),
            list(map(Write, [f_brace.label, dx_brace.label])),
        ))
        self.wait()
        for i in range(start_rect_index+1, last_rect_index):
            self.play(
                rects[i-1].set_fill, None, low_opacity,
                rects[i].set_fill, None, 1,
                f_brace.set_height, rects[i].get_height(),
                f_brace.next_to, rects[i], LEFT, 0,
                dx_brace.next_to, rects[i], DOWN, 0,
                *[
                    MaintainPositionRelativeTo(brace.label, brace)
                    for brace in (f_brace, dx_brace)
                ]
            )
        self.wait()
        self.play(*it.chain(
            list(map(FadeOut, [
                f_brace, dx_brace, 
                f_brace.label, dx_brace.label
            ])),
            [rects.set_fill, None, kwargs["fill_opacity"]]
        ))

    def show_rects_approaching_area(self):
        for new_rects in self.rect_list:
            self.transform_between_riemann_rects(
                self.rects, new_rects
            )

    def write_antiderivative(self):
        deriv = OldTex(
            "{d", "F", "\\over\\,", "dx}", "(x)", "=", "f(x)"
        )
        deriv_F = deriv.get_part_by_tex("F")
        deriv.next_to(self.integral, DOWN, MED_LARGE_BUFF)
        rhs = OldTex(*"=F(b)-F(a)")
        rhs.set_color_by_tex("a", self.lower_bound_color)
        rhs.set_color_by_tex("b", self.upper_bound_color)
        rhs.next_to(self.integral, RIGHT)

        self.play(Write(deriv))
        self.wait(2)
        self.play(*it.chain(
            [
                ReplacementTransform(deriv_F.copy(), part)
                for part in rhs.get_parts_by_tex("F")
            ],
            [
                Write(VGroup(*rhs.get_parts_by_tex(tex)))
                for tex in "=()-"
            ]
        ))
        for tex in "b", "a":
            self.play(ReplacementTransform(
                self.integral.get_part_by_tex(tex).copy(),
                rhs.get_part_by_tex(tex)
            ))
            self.wait()
        self.wait(2)

        self.deriv = deriv
        self.rhs = rhs

    def write_fundamental_theorem_of_calculus(self):
        words = OldTexText("""
            Fundamental 
            theorem of 
            calculus
        """)
        words.to_edge(RIGHT)

        self.play(Write(words))
        self.wait()

    def show_integral_considering_continuum(self):
        self.play(*[
            ApplyMethod(mob.set_fill, None, 0.2)
            for mob in (self.deriv, self.rhs)
        ])
        self.play(
            self.rects.restore,
            run_time = 3,
            rate_func = there_and_back
        )
        self.wait()
        for x in range(2):
            self.play(*[
                ApplyFunction(
                    lambda m : m.shift(MED_SMALL_BUFF*UP).set_fill(opacity = 1),
                    rect,
                    run_time = 3,
                    rate_func = squish_rate_func(
                        there_and_back,
                        alpha, alpha+0.2
                    )
                )
                for rect, alpha in zip(
                    self.rects, 
                    np.linspace(0, 0.8, len(self.rects))
                )
            ])
        self.wait()

    def show_antiderivative_considering_bounds(self):
        self.play(
            self.integral.set_fill, None, 0.5,
            self.deriv.set_fill, None, 1,
            self.rhs.set_fill, None, 1,
        )
        for label, line in reversed(list(zip(self.bound_labels, self.v_lines))):
            new_line = line.copy().set_color(YELLOW)
            label.save_state()
            self.play(label.set_color, YELLOW)
            self.play(ShowCreation(new_line))
            self.play(ShowCreation(line))
            self.remove(new_line)
            self.play(label.restore)
        self.wait()
        self.play(self.integral.set_fill, None, 1)
        self.wait(3)
