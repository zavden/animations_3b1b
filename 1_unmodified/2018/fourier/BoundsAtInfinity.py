# ==============================================================================
# Scene:      BoundsAtInfinity
# Source:     videos/_2018/fourier.py (lines 3833-3945)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BoundsAtInfinity.py BoundsAtInfinity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SummarizeFormula(Scene):
    def construct(self):
        expression = self.get_expression()
        screen_rect = ScreenRectangle(height = 5)
        screen_rect.to_edge(DOWN)

        exp_rect, g_exp_rect, int_rect = [
            SurroundingRectangle(VGroup(
                expression.get_part_by_tex(p1),
                expression.get_part_by_tex(p2),
            ))
            for p1, p2 in [("e", "t}"), ("g({}", "t}"), ("\\int", "dt")]
        ]

        self.add(expression)
        self.wait()
        self.play(
            ShowCreation(screen_rect),
            ShowCreation(exp_rect),
        )
        self.wait(2)
        self.play(Transform(exp_rect, g_exp_rect))
        self.wait(2)
        self.play(Transform(exp_rect, int_rect))
        self.wait(2)

    def get_expression(self):
        expression = OldTex(
            "\\hat g(", "f", ")", "=", "\\int", "_{t_1}", "^{t_2}",
            "g({}", "t", ")", "e", "^{-2\\pi i", "f", "t}", "dt"
        )
        expression.set_color_by_tex(
            "t", YELLOW, substring = False,
        )
        expression.set_color_by_tex("t}", YELLOW)
        expression.set_color_by_tex(
            "f", RED, substring = False,
        )
        expression.scale(1.2)
        expression.to_edge(UP)
        return expression


class BoundsAtInfinity(SummarizeFormula):
    def construct(self):
        expression = self.get_expression()
        self.add(expression)
        self.add_graph()
        axes = self.axes
        graph = self.graph

        time_interval = self.get_time_interval(-2, 2)
        wide_interval = self.get_time_interval(-FRAME_X_RADIUS, FRAME_X_RADIUS)
        bounds = VGroup(*reversed(expression.get_parts_by_tex("t_")))
        bound_rects = VGroup(*[
            SurroundingRectangle(b, buff = 0.5*SMALL_BUFF)
            for b in bounds
        ])
        bound_rects.set_color(TEAL)
        inf_bounds = VGroup(*[
            VGroup(OldTex(s + "\\infty"))
            for s in ("-", "+")
        ])
        decimal_bounds = VGroup(*[DecimalNumber(0) for x in range(2)])
        for bound, inf_bound, d_bound in zip(bounds, inf_bounds, decimal_bounds):
            for new_bound in inf_bound, d_bound:
                new_bound.scale(0.7)
                new_bound.move_to(bound, LEFT)
                new_bound.bound = bound
        def get_db_num_update(vect):
            return lambda a : axes.x_axis.point_to_number(
                time_interval.get_edge_center(vect)
            )
        decimal_updates = [
            ChangingDecimal(
                db, get_db_num_update(vect),
                position_update_func = lambda m : m.move_to(
                    m.bound, LEFT
                )
            )
            for db, vect in zip(decimal_bounds, [LEFT, RIGHT])
        ]
        for update in decimal_updates:
            update.update(1)

        time_interval.save_state()
        self.wait()
        self.play(ReplacementTransform(
            self.get_time_interval(0, 0.01), time_interval
        ))
        self.play(LaggedStartMap(ShowCreation, bound_rects))
        self.wait()
        self.play(FadeOut(bound_rects))
        self.play(ReplacementTransform(bounds, inf_bounds))
        self.play(Transform(
            time_interval, wide_interval,
            run_time = 4,
            rate_func = there_and_back
        ))
        self.play(
            ReplacementTransform(inf_bounds, decimal_bounds),
            time_interval.restore,
        )
        self.play(
            VGroup(axes, graph).stretch, 0.05, 0,
            Transform(time_interval, wide_interval),
            UpdateFromAlphaFunc(
                axes.x_axis.numbers, 
                lambda m, a : m.set_fill(opacity = 1-a)
            ),
            *decimal_updates,
            run_time = 12,
            rate_func = bezier([0, 0, 1, 1])
        )
        self.wait()


    def add_graph(self):
        axes = Axes(
            x_min = -140,
            x_max = 140,
            y_min = -2, 
            y_max = 2,
            axis_config = {
                "include_tip" : False,
            },
        )
        axes.x_axis.add_numbers(*list(filter(
            lambda x : x != 0,
            list(range(-8, 10, 2)),
        )))
        axes.shift(DOWN)
        self.add(axes)

        def func(x):
            return np.exp(-0.1*x**2)*(1 + np.cos(TAU*x))
        graph = axes.get_graph(func)
        self.add(graph)
        graph.set_color(YELLOW)

        self.set_variables_as_attrs(axes, graph)

    def get_time_interval(self, t1, t2):
        line = Line(*[
            self.axes.coords_to_point(t, 0)
            for t in (t1, t2)
        ])
        rect = Rectangle(
            stroke_width = 0,
            fill_color = TEAL,
            fill_opacity = 0.5,
        )
        rect.match_width(line)
        rect.stretch_to_fit_height(2.5)
        rect.move_to(line, DOWN)
        return rect
