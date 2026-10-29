# ==============================================================================
# Scene:      GraphLimitExpression
# Source:     videos/_2017/eoc/chapter7.py (lines 755-1198)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GraphLimitExpression.py GraphLimitExpression -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo animations absorbed unknown kwargs (digest_config); here `added_anims` must not reach UpdateFromAlphaFunc: pop it
#   - Cairo smooth(t, inflection): cairo_smooth
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class GraphLimitExpression(GraphScene):
    CONFIG = {
        "start_x" : 2,
        "h_color" : GREEN,
        "f_color" : YELLOW,
        "two_color" : RED,
        "graph_origin" : 3*DOWN+LEFT,
        "x_min" : -8,
        "x_max" : 5,
        "x_axis_label" : "$h$",
        "x_labeled_nums" : list(range(-8, 6, 2)),
        "y_min" : 0,
        "y_max" : 20,
        "y_tick_frequency" : 1,
        "y_labeled_nums" : list(range(5, 25, 5)),
        "y_axis_label" : "",
        "big_delta" : 0.7,
        "small_delta" : 0.01,
    }
    def construct(self):
        self.func = lambda h : 3*(2**2) + 3*2*h + h**2
        self.setup_axes()
        self.introduce_function()
        self.emphasize_non_definedness_at_0()
        self.draw_limit_point_hole()
        self.show_limit()
        self.skeptic_asks()
        self.show_epsilon_delta_intuition()

    def introduce_function(self):
        expression = OldTex(
            "{(", "2", "+", "h", ")", "^3",
            "-", "(", "2", ")", "^3",
            "\\over \\,", "h}",
            arg_separator = "",
        )
        limit = OldTex("\\lim", "_{h", "\\to 0}")
        derivative = OldTex(
            "{d(x^3)", "\\over \\,", "dx}", "(", "2", ")"
        )
        tex_to_color = {
            "h" : self.h_color,
            "dx" : self.h_color,
            "2" : self.two_color
        }
        for tex_mob in expression, limit, derivative:
            for tex, color in list(tex_to_color.items()):
                tex_mob.set_color_by_tex(tex, color)
            tex_mob.next_to(ORIGIN, RIGHT, LARGE_BUFF)
            tex_mob.to_edge(UP)

        expression.save_state()
        expression.generate_target()
        expression.target.next_to(limit, RIGHT)
        brace = Brace(VGroup(limit, expression.target))
        derivative.next_to(brace, DOWN)



        indices = [0, 6, 11, 13]
        funcs = [
            lambda h : (2+h)**3,
            lambda h : (2+h)**3 - 2**3,
            self.func
        ]
        graph = None
        for i, j, func in zip(indices, indices[1:], funcs):
            anims = [FadeIn(
                VGroup(*expression[i:j]),
                lag_ratio = 0.5,
            )]
            new_graph = self.get_graph(func, color = BLUE)
            if graph is None:
                graph = new_graph
                anims.append(FadeIn(graph))
            else:
                anims.append(Transform(graph, new_graph))
            self.play(*anims)
            self.wait()
        self.wait()
        self.play(
            MoveToTarget(expression),
            FadeIn(limit, lag_ratio = 0.5),
            GrowFromCenter(brace)
        )
        self.play(Write(derivative))
        self.wait(2)
        self.play(
            expression.restore,
            *list(map(FadeOut, [derivative, brace, limit]))
        )
        self.wait()

        colored_graph = graph.copy().set_color(YELLOW)
        self.play(ShowCreation(colored_graph))
        self.wait()
        self.play(ShowCreation(graph))
        self.remove(colored_graph)
        self.wait()

        self.expression = expression
        self.limit = limit
        self.graph = graph

    def emphasize_non_definedness_at_0(self):
        expression = self.expression
        
        dot = Dot(self.graph_origin, color = GREEN)
        h_equals_0 = OldTex("h", "=", "0", "?")
        h_equals_0.next_to(self.graph_origin, UP+RIGHT, LARGE_BUFF)
        for tex in "h", "0":
            h_equals_0.set_color_by_tex(tex, GREEN)

        arrow = Arrow(h_equals_0.get_left(), self.graph_origin)
        arrow.set_color(WHITE)

        new_expression = expression.deepcopy()
        h_group = VGroup(*new_expression.get_parts_by_tex("h"))
        for h in h_group:
            zero = OldTex("0")
            zero.set_color(h.get_color())
            zero.replace(h, dim_to_match = 1)
            Transform(h, zero).update(1)
        rhs = OldTex("=", "{\\, 0\\,", "\\over \\,", "0\\,}")
        rhs.set_color_by_tex("0", GREEN)
        rhs.next_to(new_expression, RIGHT)
        equation = VGroup(new_expression, rhs)
        equation.next_to(expression, DOWN, buff = LARGE_BUFF)

        ud_brace = Brace(VGroup(*rhs[1:]), DOWN)
        undefined = OldTexText("Undefined")
        undefined.next_to(ud_brace, DOWN)
        undefined.to_edge(RIGHT)

        self.play(Write(h_equals_0, run_time = 2))
        self.play(*list(map(ShowCreation, [arrow, dot])))
        self.wait()
        self.play(ReplacementTransform(
            expression.copy(), new_expression
        ))
        self.wait()
        self.play(Write(rhs))
        self.wait()
        self.play(
            GrowFromCenter(ud_brace),
            Write(undefined)
        )
        self.wait(2)

        self.point_to_zero_group = VGroup(
            h_equals_0, arrow, dot
        )
        self.plug_in_zero_group = VGroup(
            new_expression, rhs, ud_brace, undefined
        )

    def draw_limit_point_hole(self):
        dx = 0.07
        color = self.graph.get_color()
        circle = Circle(
            radius = dx, 
            stroke_color = color,
            fill_color = BLACK,
            fill_opacity = 1,
        )
        circle.move_to(self.coords_to_point(0, 12))
        colored_circle = circle.copy()
        colored_circle.set_stroke(YELLOW)
        colored_circle.set_fill(opacity = 0)

        self.play(GrowFromCenter(circle))
        self.wait()
        self.play(ShowCreation(colored_circle))
        self.play(ShowCreation(
            circle.copy().set_fill(opacity = 0),
            remover = True
        ))
        self.remove(colored_circle)
        self.play(
            circle.scale, 0.3,
            run_time = 2,
            rate_func = wiggle
        )
        self.wait()

        self.limit_point_hole = circle

    def show_limit(self):
        dot = self.point_to_zero_group[-1]
        ed_group = self.get_epsilon_delta_group(self.big_delta)

        left_v_line, right_v_line = ed_group.delta_lines
        bottom_h_line, top_h_line = ed_group.epsilon_lines
        ed_group.delta_lines.save_state()
        ed_group.epsilon_lines.save_state()

        brace = Brace(ed_group.input_range, UP)
        brace_text = brace.get_text("Inputs around 0", buff = SMALL_BUFF)
        brace_text.add_background_rectangle()
        brace_text.shift(RIGHT)

        limit_point_hole_copy = self.limit_point_hole.copy()
        limit_point_hole_copy.set_stroke(YELLOW)
        h_zero_hole = limit_point_hole_copy.copy()
        h_zero_hole.move_to(self.graph_origin)

        ed_group.input_range.add(h_zero_hole)
        ed_group.output_range.add(limit_point_hole_copy)

        #Show range around 0
        self.play(
            FadeOut(self.plug_in_zero_group),
            FadeOut(VGroup(*self.point_to_zero_group[:-1])),
        )
        self.play(
            GrowFromCenter(brace),
            Write(brace_text),
            ReplacementTransform(dot, ed_group.input_range),
        )
        self.add(h_zero_hole)
        self.wait()
        self.play(
            ReplacementTransform(
                ed_group.input_range.copy(), 
                ed_group.output_range, 
                run_time = 2
            ),
        )
        self.remove(self.limit_point_hole)

        #Show approaching
        self.play(*list(map(FadeOut, [brace, brace_text])))
        for v_line, h_line in (right_v_line, top_h_line), (left_v_line, bottom_h_line):
            self.play(
                ShowCreation(v_line),
                ShowCreation(h_line)
            )
            self.wait()
            self.play(
                v_line.move_to, self.coords_to_point(0, 0), DOWN,
                h_line.move_to, self.coords_to_point(0, self.func(0)),
                run_time = 3
            )
            self.play(
                VGroup(h_line, v_line).set_stroke, GREY, 2,
            )
        self.wait()

        #Write limit
        limit = self.limit
        limit.next_to(self.expression, LEFT)
        equals, twelve = rhs = OldTex("=", "12")
        rhs.next_to(self.expression, RIGHT)
        twelve_copy = twelve.copy()
        limit_group = VGroup(limit, rhs)

        self.play(Write(limit_group))
        self.wait()
        self.play(twelve_copy.next_to, top_h_line, RIGHT)
        self.wait()

        self.twelve_copy = twelve_copy
        self.rhs = rhs
        self.ed_group = ed_group
        self.input_range_brace_group = VGroup(brace, brace_text)

    def skeptic_asks(self):
        randy = Randolph()
        randy.scale(0.9)
        randy.to_edge(DOWN)

        self.play(FadeIn(randy))
        self.play(PiCreatureSays(
            randy, """
                What \\emph{exactly} do you
                mean by ``approach''
            """,
            bubble_config = {
                "height" : 3,
                "width" : 5,
                "fill_opacity" : 1,
                "direction" : LEFT,
            },
            target_mode = "sassy"
        ))
        self.remove(self.twelve_copy)
        self.play(randy.look, OUT)
        self.play(Blink(randy))
        self.wait()
        self.play(RemovePiCreatureBubble(
            randy, target_mode = "pondering",
            look_at = self.limit_point_hole
        ))
        self.play(
            self.ed_group.delta_lines.restore,
            self.ed_group.epsilon_lines.restore,
            Animation(randy),
            rate_func = there_and_back,
            run_time = 5,
        )
        self.play(Blink(randy))
        self.play(FadeOut(randy))

    def show_epsilon_delta_intuition(self):
        self.play(
            FadeOut(self.ed_group.epsilon_lines),
            FadeIn(self.input_range_brace_group)
        )
        self.ed_group.epsilon_lines.restore()
        self.wait()
        self.play(
            self.ed_group.delta_lines.restore, 
            Animation(self.input_range_brace_group),
            run_time = 2
        )
        self.play(FadeOut(self.input_range_brace_group))
        self.play(
            ReplacementTransform(
                self.ed_group.input_range.copy(),
                self.ed_group.output_range,
                run_time = 2
            )
        )
        self.wait()
        self.play(*list(map(GrowFromCenter, self.ed_group.epsilon_lines)))
        self.play(*[
            ApplyMethod(
                line.copy().set_stroke(GREY, 2).move_to,
                self.coords_to_point(0, self.func(0)),
                run_time = 3,
                rate_func = there_and_back,
                remover = True,
            )
            for line in self.ed_group.epsilon_lines
        ])
        self.wait()

        holes = VGroup(
            self.ed_group.input_range.submobjects.pop(),
            self.ed_group.output_range.submobjects.pop(),
        )
        holes.save_state()
        self.animate_epsilon_delta_group_change(
            self.ed_group,
            target_delta = self.small_delta,
            run_time = 8,
            # CHANGE: Cairo smooth(t, inflection): cairo_smooth
            rate_func = lambda t : cairo_smooth(t, 2),
            added_anims = [
                ApplyMethod(
                    hole.scale, 0.5,
                    run_time = 8
                )
                for hole in holes
            ]
        )
        self.wait()

        self.holes = holes

    #########

    def get_epsilon_delta_group(
        self, 
        delta,
        limit_x = 0,
        dashed_line_stroke_width = 3,
        dashed_line_length = FRAME_HEIGHT,
        input_range_color = YELLOW,
        input_range_stroke_width = 6,
        ):
        kwargs = dict(locals())
        result = VGroup()
        kwargs.pop("self")
        result.delta = kwargs.pop("delta")
        result.limit_x = kwargs.pop("limit_x")
        result.kwargs = kwargs
        dashed_line = DashedLine(
            ORIGIN, dashed_line_length*RIGHT,
            stroke_width = dashed_line_stroke_width
        )
        x_values = [limit_x-delta, limit_x+delta]
        x_axis_points = [self.coords_to_point(x, 0) for x in x_values]
        result.delta_lines = VGroup(*[
            dashed_line.copy().rotate(np.pi/2).move_to(
                point, DOWN
            )
            for point in x_axis_points
        ])
        if self.func(limit_x) < 0:
            result.delta_lines.rotate(
                np.pi, RIGHT, 
                about_point = result.delta_lines.get_bottom()
            )
        basically_zero = 0.00001
        result.input_range, result.output_range = [
            VGroup(*[
                self.get_graph(
                    func,
                    color = input_range_color,
                    x_min = x_min,
                    x_max = x_max,
                )
                for x_min, x_max in [
                    (limit_x-delta, limit_x-basically_zero),
                    (limit_x+basically_zero, limit_x+delta),
                ]
            ]).set_stroke(width = input_range_stroke_width)
            for func in ((lambda h : 0), self.func)
        ]
        result.epsilon_lines = VGroup(*[
            dashed_line.copy().move_to(
                self.coords_to_point(limit_x, 0)[0]*RIGHT+\
                result.output_range.get_edge_center(vect)[1]*UP
            )
            for vect in (DOWN, UP)
        ])

        result.digest_mobject_attrs()
        return result

    def animate_epsilon_delta_group_change(
        self, epsilon_delta_group, target_delta,
        **kwargs
        ):
        # CHANGE: Cairo animations absorbed unknown kwargs (digest_config); here `added_anims` must not reach UpdateFromAlphaFunc: pop it
        added_anims = kwargs.pop("added_anims", [])
        limit_x = epsilon_delta_group.limit_x
        start_delta = epsilon_delta_group.delta
        ed_group_kwargs = epsilon_delta_group.kwargs
        def update_ed_group(ed_group, alpha):
            delta = interpolate(start_delta, target_delta, alpha)
            new_group = self.get_epsilon_delta_group(
                delta, limit_x = limit_x,
                **ed_group_kwargs
            )
            Transform(ed_group, new_group).update(1)
            return ed_group

        self.play(
            UpdateFromAlphaFunc(
                epsilon_delta_group, update_ed_group,
                **kwargs
            ),
            *added_anims
        )
