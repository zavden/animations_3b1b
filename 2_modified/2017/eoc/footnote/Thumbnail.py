# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2017/eoc/footnote.py (lines 872-891)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/eoc/chapter1.py, _2017/eoc/chapter10.py, _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - smooth/rush_* with `inflection` are the Cairo rate functions (cairo_smooth in cairo_compat)
#   - Python 2 integer division used as list index
# ==============================================================================

import math
from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

DISTANCE_COLOR = BLUE


TIME_COLOR = YELLOW


VELOCITY_COLOR = GREEN


class GraphCarTrajectory(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_max" : 10,
        "x_labeled_nums" : list(range(1, 11)),
        "x_axis_label" : "Time (seconds)",
        "y_min" : 0,
        "y_max" : 110,
        "y_tick_frequency" : 10,
        "y_labeled_nums" : list(range(10, 110, 10)),
        "y_axis_label" : "Distance traveled \\\\ (meters)",
        "graph_origin" : 2.5*DOWN + 5*LEFT,
        "default_graph_colors" : [DISTANCE_COLOR, VELOCITY_COLOR],
        "default_derivative_color" : VELOCITY_COLOR,
        "time_of_journey" : 10,
        "care_movement_rate_func" : smooth,
    }
    def construct(self):
        self.setup_axes(animate = False)
        graph = self.graph_sigmoid_trajectory_function()
        origin = self.coords_to_point(0, 0)

        self.introduce_graph(graph, origin)
        self.comment_on_slope(graph, origin)
        self.show_velocity_graph()
        self.ask_critically_about_velocity()

    def graph_sigmoid_trajectory_function(self, **kwargs):
        graph = self.get_graph(
            lambda t : 100*smooth(t/10.),
            **kwargs
        )
        self.s_graph = graph
        return graph

    def introduce_graph(self, graph, origin):
        h_line, v_line = [
            Line(origin, origin, color = color, stroke_width = 2)
            for color in (TIME_COLOR, DISTANCE_COLOR)
        ]
        def h_update(h_line, proportion = 1):
            end = graph.point_from_proportion(proportion)
            t_axis_point = end[0]*RIGHT + origin[1]*UP
            h_line.put_start_and_end_on(t_axis_point, end)
        def v_update(v_line, proportion = 1):
            end = graph.point_from_proportion(proportion)
            d_axis_point = origin[0]*RIGHT + end[1]*UP
            v_line.put_start_and_end_on(d_axis_point, end)

        car = Car()
        car.rotate(np.pi/2)
        car.move_to(origin)
        car_target = origin*RIGHT + graph.point_from_proportion(1)*UP


        self.add(car)
        self.play(
            ShowCreation(
                graph,
                rate_func=linear,
            ),
            MoveCar(
                car, car_target,
                rate_func = self.care_movement_rate_func
            ),
            UpdateFromFunc(h_line, h_update),
            UpdateFromFunc(v_line, v_update),
            run_time = self.time_of_journey,
        )
        self.wait()
        self.play(*list(map(FadeOut, [h_line, v_line, car])))

        #Show example vertical distance
        h_update(h_line, 0.6)
        t_dot = Dot(h_line.get_start(), color = h_line.get_color())
        t_dot.save_state()
        t_dot.move_to(self.x_axis_label_mob)
        t_dot.set_fill(opacity = 0)
        dashed_h = DashedLine(*h_line.get_start_and_end())
        dashed_h.set_color(h_line.get_color())
        brace = Brace(dashed_h, RIGHT)
        brace_text = brace.get_text("Distance traveled")
        self.play(t_dot.restore)
        self.wait()
        self.play(ShowCreation(dashed_h))
        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [t_dot, dashed_h, brace, brace_text])))

        #Name graph
        s_of_t = OldTex("s(t)")
        s_of_t.next_to(
            graph.point_from_proportion(1), 
            DOWN+RIGHT,
            buff = SMALL_BUFF
        )
        s = s_of_t[0]
        d = OldTex("d")
        d.move_to(s, DOWN)
        d.set_color(DISTANCE_COLOR)

        self.play(Write(s_of_t))
        self.wait()
        s.save_state()
        self.play(Transform(s, d))
        self.wait()
        self.play(s.restore)

    def comment_on_slope(self, graph, origin):
        delta_t = 1
        curr_time = 0
        ghost_line = Line(
            origin, 
            self.coords_to_point(delta_t, self.y_max)
        )
        rect = Rectangle().replace(ghost_line, stretch = True)
        rect.set_stroke(width = 0)
        rect.set_fill(TIME_COLOR, opacity = 0.3)

        change_lines = self.get_change_lines(curr_time, delta_t)
        self.play(FadeIn(rect))
        self.wait()
        self.play(Write(change_lines))
        self.wait()
        for x in range(1, 10):
            curr_time = x
            new_change_lines = self.get_change_lines(curr_time, delta_t)
            self.play(
                rect.move_to, self.coords_to_point(curr_time, 0), DOWN+LEFT,
                Transform(change_lines, new_change_lines)
            )
            if curr_time == 5:
                text = change_lines[-1].get_text(
                    "$\\frac{\\text{meters}}{\\text{second}}$"
                )
                self.play(Write(text))
                self.wait()
                self.play(FadeOut(text))
            else:
                self.wait()
        self.play(*list(map(FadeOut, [rect, change_lines])))
        self.rect = rect

    def get_change_lines(self, curr_time, delta_t = 1):
        p1 = self.input_to_graph_point(
            curr_time, self.s_graph
        )
        p2 = self.input_to_graph_point(
            curr_time+delta_t, self.s_graph
        )
        interim_point = p2[0]*RIGHT + p1[1]*UP
        delta_t_line = Line(p1, interim_point, color = TIME_COLOR)
        delta_s_line = Line(interim_point, p2, color = DISTANCE_COLOR)
        brace = Brace(delta_s_line, RIGHT, buff = SMALL_BUFF)
        return VGroup(delta_t_line, delta_s_line, brace)

    def show_velocity_graph(self):
        velocity_graph = self.get_derivative_graph(self.s_graph)

        self.play(ShowCreation(velocity_graph))
        def get_velocity_label(v_graph):
            result = self.get_graph_label(
                v_graph,
                label = "v(t)",
                direction = UP+RIGHT,
                x_val = 5,
                buff = SMALL_BUFF,
            )
            self.remove(result)
            return result
        label = get_velocity_label(velocity_graph)
        self.play(Write(label))
        self.wait()
        self.rect.move_to(self.coords_to_point(0, 0), DOWN+LEFT)
        self.play(FadeIn(self.rect))
        self.wait()
        for time, show_slope in (4.5, True), (9, False):
            self.play(
                self.rect.move_to, self.coords_to_point(time, 0), DOWN+LEFT
            )
            if show_slope:
                change_lines = self.get_change_lines(time)
                self.play(FadeIn(change_lines))
                self.wait()
                self.play(FadeOut(change_lines))
            else:
                self.wait()
        self.play(FadeOut(self.rect))

        #Change distance and velocity graphs
        self.s_graph.save_state()
        velocity_graph.save_state()
        label.save_state()
        def shallow_slope(t):
            # CHANGE: smooth/rush_* with `inflection` are the Cairo rate functions (cairo_smooth in cairo_compat)
            return 100*cairo_smooth(t/10., inflection = 4)
        def steep_slope(t):
            # CHANGE: smooth/rush_* with `inflection` are the Cairo rate functions (cairo_smooth in cairo_compat)
            return 100*cairo_smooth(t/10., inflection = 25)
        def double_smooth_graph_function(t):
            if t < 5:
                return 50*smooth(t/5.)
            else:
                return 50*(1+smooth((t-5)/5.))
        graph_funcs = [
            shallow_slope,
            steep_slope,
            double_smooth_graph_function,
        ]
        for graph_func in graph_funcs:
            new_graph = self.get_graph(
                graph_func,
                color = DISTANCE_COLOR,
            )
            self.remove(new_graph)
            new_velocity_graph = self.get_derivative_graph(
                graph = new_graph,
            )
            new_velocity_label = get_velocity_label(new_velocity_graph)

            self.play(Transform(self.s_graph, new_graph))
            self.play(
                Transform(velocity_graph, new_velocity_graph),
                Transform(label, new_velocity_label),
            )
            self.wait(2)
        self.play(self.s_graph.restore)
        self.play(
            velocity_graph.restore,
            label.restore,
        )
        self.wait(2)

    def ask_critically_about_velocity(self):
        morty = Mortimer().flip()
        morty.to_corner(DOWN+LEFT)
        self.play(PiCreatureSays(morty,
            "Think critically about \\\\",
            "what velocity means."
        ))
        self.play(Blink(morty))
        self.wait()


class DefineTrueDerivative(Scene):
    def construct(self):
        title = OldTexText("The true derivative")
        title.to_edge(UP)

        lhs = OldTex("\\frac{ds}{dt}(t) = ")
        VGroup(*lhs[:2]).set_color(DISTANCE_COLOR)
        VGroup(*lhs[3:5]).set_color(TIME_COLOR)
        lhs.shift(3*LEFT+UP)

        dt_rhs = self.get_fraction("dt")
        numerical_rhs_list = [
            self.get_fraction("0.%s1"%("0"*x))
            for x in range(7)
        ]
        for rhs in [dt_rhs] + numerical_rhs_list:
            rhs.next_to(lhs, RIGHT)

        brace, dt_to_zero = self.get_brace_and_text(dt_rhs)

        self.add(lhs, dt_rhs)
        self.play(Write(title))
        self.wait()
        dt_rhs.save_state()
        for num_rhs in numerical_rhs_list:
            self.play(Transform(dt_rhs, num_rhs))
        self.wait()
        self.play(dt_rhs.restore)
        self.play(
            GrowFromCenter(brace),
            Write(dt_to_zero)
        )
        self.wait()

    def get_fraction(self, dt_string):
        tex_mob = OldTex(
            "\\frac{s(t + %s) - s(t)}{%s}"%(dt_string, dt_string)
        )
        part_lengths = [
            0,
            len("s(t+"),
            1,#1 and -1 below are purely for transformation quirks
            len(dt_string)-1,
            len(")-s(t)_"),#Underscore represents frac_line
            1,
            len(dt_string)-1,
        ]
        pl_cumsum = np.cumsum(part_lengths)
        result = VGroup(*[
            VGroup(*tex_mob[i1:i2])
            for i1, i2 in zip(pl_cumsum, pl_cumsum[1:])
        ])
        VGroup(*result[1:3]+result[4:6]).set_color(TIME_COLOR)
        return result

    def get_brace_and_text(self, deriv_frac):
        brace = Brace(VGroup(deriv_frac), DOWN)
        dt_to_zero = brace.get_text("$dt \\to 0$")
        VGroup(*dt_to_zero[:2]).set_color(TIME_COLOR)
        return brace, dt_to_zero


class SecantLineToTangentLine(GraphCarTrajectory, DefineTrueDerivative):
    CONFIG = {
        "start_time" : 6,
        "end_time" : 2,
        "alt_end_time" : 10,
        "start_dt" : 2,
        "end_dt" : 0.01,
        "secant_line_length" : 10,

    }
    def construct(self):
        self.setup_axes(animate = False)
        self.remove(self.y_axis_label_mob, self.x_axis_label_mob)
        self.add_derivative_definition(self.y_axis_label_mob)
        self.add_graph()
        self.draw_axes()
        self.show_tangent_line()
        self.best_constant_approximation_around_a_point()

    def get_ds_dt_group(self, dt, animate = False):
        points = [
            self.input_to_graph_point(time, self.graph)
            for time in (self.curr_time, self.curr_time+dt)
        ]
        dots = list(map(Dot, points))
        for dot in dots:
            dot.scale(0.5)
        secant_line = Line(*points)
        secant_line.set_color(VELOCITY_COLOR)
        secant_line.scale(
            self.secant_line_length/secant_line.get_length()
        )

        interim_point = points[1][0]*RIGHT + points[0][1]*UP
        dt_line = Line(points[0], interim_point, color = TIME_COLOR)
        ds_line = Line(interim_point, points[1], color = DISTANCE_COLOR)
        dt = OldTex("dt")
        dt.set_color(TIME_COLOR)
        if dt.get_width() > dt_line.get_width():
            dt.scale(
                dt_line.get_width()/dt.get_width(),
                about_point = dt.get_top()
            )
        dt.next_to(dt_line, DOWN, buff = SMALL_BUFF)
        ds = OldTex("ds")
        ds.set_color(DISTANCE_COLOR)
        if ds.get_height() > ds_line.get_height():
            ds.scale(
                ds_line.get_height()/ds.get_height(),
                about_point = ds.get_left()
            )
        ds.next_to(ds_line, RIGHT, buff = SMALL_BUFF)

        group = VGroup(
            secant_line, 
            ds_line, dt_line,
            ds, dt,
            *dots
        )
        if animate:
            self.play(
                ShowCreation(dt_line),
                Write(dt),
                ShowCreation(dots[0]),                
            )
            self.play(
                ShowCreation(ds_line),
                Write(ds),
                ShowCreation(dots[1]),                
            )
            self.play(
                ShowCreation(secant_line),
                Animation(VGroup(*dots))
            )
        return group

    def add_graph(self):
        def double_smooth_graph_function(t):
            if t < 5:
                return 50*smooth(t/5.)
            else:
                return 50*(1+smooth((t-5)/5.))
        self.graph = self.get_graph(double_smooth_graph_function)
        self.graph_label = self.get_graph_label(
            self.graph, "s(t)", 
            x_val = self.x_max, 
            direction = DOWN+RIGHT, 
            buff = SMALL_BUFF,
        )

    def add_derivative_definition(self, target_upper_left):
        deriv_frac = self.get_fraction("dt")
        lhs = OldTex("\\frac{ds}{dt}(t)=")
        VGroup(*lhs[:2]).set_color(DISTANCE_COLOR)
        VGroup(*lhs[3:5]).set_color(TIME_COLOR)
        lhs.next_to(deriv_frac, LEFT)
        brace, text = self.get_brace_and_text(deriv_frac)
        deriv_def = VGroup(lhs, deriv_frac, brace, text)
        deriv_word = OldTexText("Derivative")        
        deriv_word.next_to(deriv_def, UP, buff = MED_LARGE_BUFF)
        deriv_def.add(deriv_word)
        rect = Rectangle(color = WHITE)
        rect.replace(deriv_def, stretch = True)
        rect.scale(1.2)
        deriv_def.add(rect)
        deriv_def.scale(0.7)
        deriv_def.move_to(target_upper_left, UP+LEFT)
        self.add(deriv_def)
        return deriv_def

    def draw_axes(self):
        self.x_axis.remove(self.x_axis_label_mob)
        self.y_axis.remove(self.y_axis_label_mob)
        self.play(Write(
            VGroup(
                self.x_axis, self.y_axis,
                self.graph, self.graph_label
            ),
            run_time = 4
        ))
        self.wait()

    def show_tangent_line(self):
        self.curr_time = self.start_time

        ds_dt_group = self.get_ds_dt_group(2, animate = True)
        self.wait()
        def update_ds_dt_group(ds_dt_group, alpha):
            new_dt = interpolate(self.start_dt, self.end_dt, alpha)
            new_group = self.get_ds_dt_group(new_dt)
            Transform(ds_dt_group, new_group).update(1)
        self.play(
            UpdateFromAlphaFunc(ds_dt_group, update_ds_dt_group),
            run_time = 15
        )
        self.wait()
        def update_as_tangent_line(ds_dt_group, alpha):
            self.curr_time = interpolate(self.start_time, self.end_time, alpha)
            new_group = self.get_ds_dt_group(self.end_dt)
            Transform(ds_dt_group, new_group).update(1)
        self.play(
            UpdateFromAlphaFunc(ds_dt_group, update_as_tangent_line),
            run_time = 8,
            rate_func = there_and_back
        )
        self.wait()
        what_dt_is_not_text = self.what_this_is_not_saying()
        self.wait()
        self.play(
            UpdateFromAlphaFunc(ds_dt_group, update_ds_dt_group),
            run_time = 8,
            rate_func = lambda t : 1-there_and_back(t)
        )
        self.wait()
        self.play(FadeOut(what_dt_is_not_text))

        v_line = self.get_vertical_line_to_graph(
            self.curr_time,
            self.graph,
            line_class = Line,
            line_kwargs = {
                "color" : MAROON_B,
                "stroke_width" : 3
            }
        )
        def v_line_update(v_line):
            v_line.put_start_and_end_on(
                self.coords_to_point(self.curr_time, 0),
                self.input_to_graph_point(self.curr_time, self.graph),
            )
            return v_line
        self.play(ShowCreation(v_line))
        self.wait()

        original_end_time = self.end_time
        for end_time in self.alt_end_time, original_end_time, self.start_time:
            self.end_time = end_time
            self.play(
                UpdateFromAlphaFunc(ds_dt_group, update_as_tangent_line),
                UpdateFromFunc(v_line, v_line_update),
                run_time = abs(self.curr_time-self.end_time),
            )
            self.start_time = end_time
        self.play(FadeOut(v_line))

    def what_this_is_not_saying(self):
        phrases = [
            OldTexText(
                "$dt$", "is", "not", s
            )
            for s in ("``infinitely small''", "0")
        ]
        for phrase in phrases:
            phrase[0].set_color(TIME_COLOR)
            phrase[2].set_color(RED)
        phrases[0].shift(DOWN+2*RIGHT)
        phrases[1].next_to(phrases[0], DOWN, aligned_edge = LEFT)

        for phrase in phrases:
            self.play(Write(phrase))
        return VGroup(*phrases)

    def best_constant_approximation_around_a_point(self):
        words = OldTexText("""
            Best constant 
            approximation
            around a point
        """)
        words.next_to(self.x_axis, UP, aligned_edge = RIGHT)
        circle = Circle(
            radius = 0.25,
            color = WHITE
        ).shift(self.input_to_graph_point(self.curr_time))

        self.play(Write(words))
        self.play(ShowCreation(circle))        
        self.wait()


class Thumbnail(SecantLineToTangentLine):
    def construct(self):
        self.setup_axes(animate = False)
        self.add_graph()
        self.curr_time = 6
        ds_dt_group = self.get_ds_dt_group(1)
        self.add(ds_dt_group)
        self.remove(self.x_axis_label_mob)
        self.remove(self.y_axis_label_mob)
        VGroup(*self.get_mobjects()).fade(0.4)

        title = OldTexText("Derivative paradox")
        title.set_width(FRAME_WIDTH-1)
        title.to_edge(UP)
        title.add_background_rectangle()
        title.set_color_by_gradient(GREEN, YELLOW)

        randy = Randolph(mode = "confused")
        randy.scale(1.7)
        randy.to_corner(DOWN+LEFT)
        randy.shift(RIGHT)

        deriv = OldTex("\\frac{ds}{dt}(t)")
        VGroup(*deriv[:2]).set_color(DISTANCE_COLOR)
        VGroup(*deriv[3:5]).set_color(TIME_COLOR)
        deriv.scale(3)
        # deriv.next_to(randy, RIGHT, buff = 2)
        deriv.to_edge(RIGHT, buff = LARGE_BUFF)
        randy.look_at(deriv)

        self.add(title, randy, deriv)



# ----- From _2017/eoc/chapter1.py -----

class AreaUnderParabola(GraphScene):
    CONFIG = {
        "x_max" : 4,
        "x_labeled_nums" : list(range(-1, 5)),
        "y_min" : 0,
        "y_max" : 15,
        "y_tick_frequency" : 2.5,
        "y_labeled_nums" : list(range(5, 20, 5)),
        "n_rect_iterations" : 6,
        "default_right_x" : 3,
        "func" : lambda x : x**2,
        "graph_label_tex" : "x^2",
        "graph_label_x_val" : 3.8,
    }
    def construct(self):
        self.setup_axes()
        self.show_graph()
        self.show_area()
        self.ask_about_area()
        self.show_confusion()
        self.show_variable_endpoint()
        self.name_integral()

    def show_graph(self):
        graph = self.get_graph(self.func)
        graph_label = self.get_graph_label(
            graph, self.graph_label_tex, 
            direction = LEFT,
            x_val = self.graph_label_x_val,
        )

        self.play(ShowCreation(graph))
        self.play(Write(graph_label))
        self.wait()

        self.graph = graph
        self.graph_label = graph_label

    def show_area(self):
        dx_list = [0.25/(2**n) for n in range(self.n_rect_iterations)]
        rect_lists = [
            self.get_riemann_rectangles(
                self.graph,
                x_min = 0,
                x_max = self.default_right_x,
                dx = dx,
                stroke_width = 4*dx,
            )
            for dx in dx_list
        ]
        rects = rect_lists[0]
        foreground_mobjects = [self.axes, self.graph]

        self.play(
            DrawBorderThenFill(
                rects,
                run_time = 2,
                rate_func = smooth,
                lag_ratio = 0.5,
            ),
            *list(map(Animation, foreground_mobjects))
        )
        self.wait()
        for new_rects in rect_lists[1:]:
            self.play(
                Transform(
                    rects, new_rects,
                    lag_ratio = 0.5,
                ), 
                *list(map(Animation, foreground_mobjects))
            )
        self.wait()

        self.rects = rects
        self.dx = dx_list[-1]
        self.foreground_mobjects = foreground_mobjects

    def ask_about_area(self):
        rects = self.rects
        question = OldTexText("Area?")
        question.move_to(rects.get_top(), DOWN)
        # CHANGE: Python 2 integer division used as list index
        mid_rect = rects[2*len(rects)//3]
        arrow = Arrow(question.get_bottom(), mid_rect.get_center())

        v_lines = VGroup(*[
            DashedLine(
                FRAME_HEIGHT*UP, ORIGIN,
                color = RED
            ).move_to(self.coords_to_point(x, 0), DOWN)
            for x in (0, self.default_right_x)
        ])

        self.play(
            Write(question),
            ShowCreation(arrow)
        )
        self.wait()
        self.play(ShowCreation(v_lines, run_time = 2))
        self.wait()

        self.foreground_mobjects += [question, arrow]
        self.question = question
        self.question_arrow = arrow
        self.v_lines = v_lines

    def show_confusion(self):
        morty = Mortimer()
        morty.to_corner(DOWN+RIGHT)

        self.play(FadeIn(morty))
        self.play(
            morty.change_mode, "confused",
            morty.look_at, self.question,
        )
        self.play(morty.look_at, self.rects.get_bottom())
        self.play(Blink(morty))
        self.play(morty.look_at, self.question)
        self.wait()
        self.play(Blink(morty))
        self.play(FadeOut(morty))

    def show_variable_endpoint(self):
        triangle = RegularPolygon(
            n = 3,
            start_angle = np.pi/2,
            stroke_width = 0,
            fill_color = WHITE,
            fill_opacity = 1,
        )
        triangle.set_height(0.25)
        triangle.move_to(self.v_lines[1].get_bottom(), UP)
        x_label = OldTex("x")
        x_label.next_to(triangle, DOWN)
        self.right_point_slider = VGroup(triangle, x_label)

        A_func = OldTex("A(x)")
        A_func.move_to(self.question, DOWN)

        self.play(FadeOut(self.x_axis.numbers))
        self.x_axis.remove(*self.x_axis.numbers)
        self.foreground_mobjects.remove(self.axes)
        self.play(DrawBorderThenFill(self.right_point_slider))
        self.move_right_point_to(2)
        self.wait()
        self.move_right_point_to(self.default_right_x)
        self.wait()
        self.play(ReplacementTransform(self.question, A_func))
        self.wait()

        self.A_func = A_func

    def name_integral(self):
        f_tex = "$%s$"%self.graph_label_tex
        words = OldTexText("``Integral'' of ", f_tex)
        words.set_color_by_tex(f_tex, self.graph_label.get_color())
        brace = Brace(self.A_func, UP)
        words.next_to(brace, UP)

        self.play(
            Write(words),
            GrowFromCenter(brace)
        )
        self.wait()
        for x in 4, 2, self.default_right_x:
            self.move_right_point_to(x, run_time = 2)

        self.integral_words_group = VGroup(brace, words)

    ####

    def move_right_point_to(self, target_x, **kwargs):
        v_line = self.v_lines[1]
        slider = self.right_point_slider
        rects = self.rects
        curr_x = self.x_axis.point_to_number(v_line.get_bottom())

        group = VGroup(rects, v_line, slider)
        def update_group(group, alpha):
            rects, v_line, slider = group
            new_x = interpolate(curr_x, target_x, alpha)
            new_rects = self.get_riemann_rectangles(
                self.graph,
                x_min = 0,
                x_max = new_x,
                dx = self.dx*new_x/3.0,
                stroke_width = rects[0].get_stroke_width(),
            )
            point = self.coords_to_point(new_x, 0)
            v_line.move_to(point, DOWN)
            slider.move_to(point, UP)
            Transform(rects, new_rects).update(1)
            return VGroup(rects, v_line, slider)

        self.play(
            UpdateFromAlphaFunc(
                group, update_group,
                **kwargs
            ),
            *list(map(Animation, self.foreground_mobjects))
        )


class PlayingTowardsDADX(AreaUnderParabola, ReconfigurableScene):
    CONFIG = {
        "n_rect_iterations" : 6,
        "deriv_dx" : 0.2,
        "graph_origin" : 2.5*DOWN + 6*LEFT,
    }
    def setup(self):
        AreaUnderParabola.setup(self)
        ReconfigurableScene.setup(self)

    def construct(self):
        self.fast_forward_to_end_of_previous_scene()

        self.nudge_x()
        self.describe_sliver()
        self.shrink_dx()
        self.write_dA_dx()
        self.dA_remains_a_mystery()
        self.write_example_inputs()
        self.show_dA_dx_in_detail()
        self.show_smaller_x()

    def fast_forward_to_end_of_previous_scene(self):
        self.force_skipping()
        AreaUnderParabola.construct(self)
        self.revert_to_original_skipping_status()

    def nudge_x(self):
        shadow_rects = self.rects.copy()
        shadow_rects.set_fill(BLACK, opacity = 0.5)

        original_v_line = self.v_lines[1].copy()
        right_v_lines = VGroup(original_v_line, self.v_lines[1])
        curr_x = self.x_axis.point_to_number(original_v_line.get_bottom())

        self.add(original_v_line)
        self.foreground_mobjects.append(original_v_line)
        self.move_right_point_to(curr_x + self.deriv_dx)
        self.play(
            FadeIn(shadow_rects), 
            *list(map(Animation, self.foreground_mobjects))
        )

        self.shadow_rects = shadow_rects
        self.right_v_lines = right_v_lines

    def describe_sliver(self):
        dx_brace = Brace(self.right_v_lines, DOWN, buff = 0)
        dx_label = dx_brace.get_text("$dx$")
        dx_group = VGroup(dx_brace, dx_label)

        dA_rect = Rectangle(
            width = self.right_v_lines.get_width(),
            height = self.shadow_rects[-1].get_height(),
            stroke_width = 0,
            fill_color = YELLOW,
            fill_opacity = 0.5,
        ).move_to(self.right_v_lines, DOWN)
        dA_label = OldTex("d", "A")
        dA_label.next_to(dA_rect, RIGHT, MED_LARGE_BUFF, UP)
        dA_label.set_color(GREEN)
        dA_arrow = Arrow(
            dA_label.get_bottom()+MED_SMALL_BUFF*DOWN, 
            dA_rect.get_center(),
            buff = 0,
            color = WHITE
        )

        difference_in_area = OldTexText(
            "d", "ifference in ", "A", "rea",
            arg_separator = ""
        )
        difference_in_area.set_color_by_tex("d", GREEN)
        difference_in_area.set_color_by_tex("A", GREEN)
        difference_in_area.scale(0.7)
        difference_in_area.next_to(dA_label, UP, MED_SMALL_BUFF, LEFT)

        side_brace = Brace(dA_rect, LEFT, buff = 0)
        graph_label_copy = self.graph_label.copy()

        self.play(
            FadeOut(self.right_point_slider),
            FadeIn(dx_group)
        )
        self.play(Indicate(dx_label))
        self.wait()
        self.play(ShowCreation(dA_arrow))
        self.wait()
        self.play(Write(dA_label, run_time = 2))
        self.wait()
        self.play(
            ReplacementTransform(dA_label[0].copy(), difference_in_area[0]),
            ReplacementTransform(dA_label[1].copy(), difference_in_area[2]),
            *list(map(FadeIn, [difference_in_area[1], difference_in_area[3]]))
        )
        self.wait(2)
        self.play(FadeIn(dA_rect), Animation(dA_arrow))
        self.play(GrowFromCenter(side_brace))
        self.play(
            graph_label_copy.set_color, WHITE,
            graph_label_copy.next_to, side_brace, LEFT, SMALL_BUFF
        )
        self.wait()
        self.play(Indicate(dx_group))
        self.wait()
        self.play(FadeOut(difference_in_area))

        self.dx_group = dx_group
        self.dA_rect = dA_rect
        self.dA_label = dA_label
        self.graph_label_copy = graph_label_copy

    def shrink_dx(self, **kwargs):
        self.transition_to_alt_config(
            deriv_dx = 0.05,
            transformation_kwargs = {"run_time" : 2},
            **kwargs
        )

    def write_dA_dx(self):
        f_tex = self.graph_label_tex
        equation = OldTex("dA", "\\approx", f_tex, "dx")
        equation.to_edge(RIGHT).shift(3*UP)
        deriv_equation = OldTex(
            "{dA", "\\over \\,", "dx}", "\\approx", f_tex
        )
        deriv_equation.move_to(equation, UP+LEFT)

        for tex_mob in equation, deriv_equation:
            tex_mob.set_color_by_tex(
                "dA", self.dA_label.get_color()
            )

        dA = VGroup(self.dA_label[0][0], self.dA_label[1][0])
        x_squared = self.graph_label_copy
        dx = self.dx_group[1]

        self.play(*[
            ReplacementTransform(
                mob.copy(),
                equation.get_part_by_tex(tex),
                run_time = 2
            )
            for mob, tex in [(x_squared, f_tex), (dx, "dx"), (dA, "dA")]
        ])
        self.play(Write(equation.get_part_by_tex("approx")))
        self.wait()
        for tex, mob in (f_tex, x_squared), ("dx", dx):
            self.play(*list(map(Indicate, [
                equation.get_part_by_tex(tex),
                mob
            ])))
            self.wait(2)
        self.play(*[
            ReplacementTransform(
                equation.get_part_by_tex(tex),
                deriv_equation.get_part_by_tex(tex),
                run_time = 2,
            )
            for tex in ("dA", "approx", f_tex, "dx")
        ] + [
            Write(deriv_equation.get_part_by_tex("over"))
        ])
        self.wait(2)
        self.shrink_dx(return_to_original_configuration = False)
        self.wait()

        self.deriv_equation = deriv_equation

    def dA_remains_a_mystery(self):
        randy = Randolph(color = BLUE_C)
        randy.to_corner(DOWN+LEFT)
        randy.look_at(self.A_func)

        A_circle, dA_circle = [
            Circle(color = color).replace(
                mob, stretch = True
            ).scale(1.5)
            for mob, color in [(self.A_func, RED), (self.deriv_equation, GREEN)]
        ]
        q_marks = OldTex("???")
        q_marks.next_to(A_circle, UP)

        self.play(
            FadeOut(self.integral_words_group),
            FadeIn(randy)
        )
        self.play(
            ShowCreation(A_circle),
            randy.change_mode, "confused"
        )
        self.play(Write(q_marks, run_time = 2))
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.change_mode, "surprised",
            randy.look_at, dA_circle,
            ReplacementTransform(A_circle, dA_circle)
        )
        self.play(Blink(randy))
        self.wait()
        self.play(*list(map(FadeOut, [randy, q_marks, dA_circle])))

    def write_example_inputs(self):
        d = self.default_right_x
        three = OldTex("x =", "%d"%d)
        three_plus_dx = OldTex("x = ", "%d.001"%d)
        labels_lines_vects = list(zip(
            [three, three_plus_dx],
            self.right_v_lines,
            [LEFT, RIGHT]
        ))

        for label, line, vect in labels_lines_vects:
            point = line.get_bottom()
            label.next_to(point, DOWN+vect, MED_SMALL_BUFF)
            label.shift(LARGE_BUFF*vect)
            label.arrow = Arrow(
                label, point,
                buff = SMALL_BUFF,
                color = WHITE,
                tip_length = 0.15
            )
            line_copy = line.copy()
            line_copy.set_color(YELLOW)

            self.play(
                FadeIn(label),
                FadeIn(label.arrow),
                ShowCreation(line_copy)
            )
            self.play(FadeOut(line_copy))
        self.wait()

        self.three = three 
        self.three_plus_dx = three_plus_dx

    def show_dA_dx_in_detail(self):
        d = self.default_right_x
        expression = OldTex(
            "{A(", "%d.001"%d, ") ", "-A(", "%d"%d, ")", 
            "\\over \\,", "0.001}", 
            "\\approx", "%d"%d, "^2"
        )
        expression.scale(0.9)
        expression.next_to(
            self.deriv_equation, DOWN, MED_LARGE_BUFF
        )
        expression.to_edge(RIGHT)

        self.play(
            ReplacementTransform(
                self.three_plus_dx.get_part_by_tex("%d.001"%d).copy(),
                expression.get_part_by_tex("%d.001"%d)
            ),
            Write(VGroup(
                expression.get_part_by_tex("A("),
                expression.get_part_by_tex(")"),
            )),
        )
        self.wait()
        self.play(
            ReplacementTransform(
                self.three.get_part_by_tex("%d"%d).copy(),
                expression.get_part_by_tex("%d"%d, substring = False)
            ),
            Write(VGroup(
                expression.get_part_by_tex("-A("),
                expression.get_parts_by_tex(")")[1],
            )),
        )
        self.wait(2)
        self.play(
            Write(expression.get_part_by_tex("over")),
            ReplacementTransform(
                expression.get_part_by_tex("%d.001"%d).copy(),
                expression.get_part_by_tex("0.001"),
            )
            
        )
        self.wait()
        self.play(
            Write(expression.get_part_by_tex("approx")),
            ReplacementTransform(
                self.graph_label_copy.copy(),
                VGroup(*expression[-2:]),
                run_time = 2
            )
        )
        self.wait()

    def show_smaller_x(self):
        self.transition_to_alt_config(
            default_right_x = 2,
            deriv_dx = 0.04,
            transformation_kwargs = {"run_time" : 2}
        )


class AlternateAreaUnderCurve(PlayingTowardsDADX):
    CONFIG = {
        "func" : lambda x : (x-2)**3 - 3*(x-2) + 6,
        "graph_label_tex" : "f(x)",
        "deriv_dx" : 0.1,
        "x_max" : 5,
        "x_axis_width" : 11,
        "graph_label_x_val" : 4.5,
    }
    def construct(self):
        #Superclass parts to skip
        self.force_skipping()
        self.setup_axes()
        self.show_graph()
        self.show_area()
        self.ask_about_area()
        self.show_confusion()

        #Superclass parts to show
        self.revert_to_original_skipping_status()
        self.show_variable_endpoint()
        self.name_integral()
        self.nudge_x()
        self.describe_sliver()
        self.write_dA_dx()

        #New animations
        self.approximation_improves_for_smaller_dx()
        self.name_derivative()

    def approximation_improves_for_smaller_dx(self):
        color = YELLOW
        approx = self.deriv_equation.get_part_by_tex("approx")
        dx_to_zero_words = OldTexText(
            "Gets better \\\\ as", 
            "$dx \\to 0$"
        )
        dx_to_zero_words.set_color_by_tex("dx", color)
        dx_to_zero_words.next_to(approx, DOWN, 1.5*LARGE_BUFF)
        arrow = Arrow(dx_to_zero_words, approx, color = color)

        self.play(
            approx.set_color, color,
            ShowCreation(arrow),
            FadeIn(dx_to_zero_words),
        )
        self.wait()
        self.transition_to_alt_config(
            deriv_dx = self.deriv_dx/4.0,
            transformation_kwargs = {"run_time" : 2}
        )

        self.dx_to_zero_words = dx_to_zero_words
        self.dx_to_zero_words_arrow = arrow

    def name_derivative(self):
        deriv_words = OldTexText("``Derivative'' of $A$")
        deriv_words.scale(0.9)
        deriv_words.to_edge(UP+RIGHT)
        moving_group = VGroup(
            self.deriv_equation, 
            self.dx_to_zero_words,
            self.dx_to_zero_words_arrow,
        )
        moving_group.generate_target()
        moving_group.target.next_to(deriv_words, DOWN, LARGE_BUFF)
        moving_group.target.to_edge(RIGHT)

        self.play(
            FadeIn(deriv_words),
            MoveToTarget(moving_group)
        )

        dA_dx = VGroup(*self.deriv_equation[:3])
        box = Rectangle(color = GREEN)
        box.replace(dA_dx, stretch = True)
        box.scale(1.3)
        brace = Brace(box, UP)
        faders = VGroup(
            self.dx_to_zero_words[0],
            self.dx_to_zero_words_arrow
        )
        dx_to_zero = self.dx_to_zero_words[1]

        self.play(*list(map(FadeIn, [box, brace])))
        self.wait()
        self.play(
            FadeOut(faders),
            dx_to_zero.next_to, box, DOWN
        )
        self.wait()


    ########
    def show_smaller_x(self):
        return

    def shrink_dx(self, **kwargs):
        return


class Thumbnail(AlternateAreaUnderCurve):
    CONFIG = {
        "x_axis_label" : "",
        "y_axis_label" : "",
        "graph_origin" : 2.4 * DOWN + 3 * LEFT,
    }
    def construct(self):
        self.setup_axes()
        self.remove(*self.x_axis.numbers)
        self.remove(*self.y_axis.numbers)
        graph = self.get_graph(self.func)
        rects = self.get_riemann_rectangles(
            graph,
            x_min = 0,
            x_max = 4,
            dx = 0.25,
            start_color = BLUE_E,
        )
        words = OldTexText("""
            Could \\emph{you} invent
            calculus?
        """)
        words.set_width(9)
        words.to_edge(UP)

        self.add(graph, rects, words)



# ----- From _2017/eoc/chapter10.py -----

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


class Thumbnail(ExampleApproximationWithSine):
    CONFIG = {
        "graph_origin" : DOWN,
        "x_axis_label" : "",
        "y_axis_label" : "",
        "x_axis_width" : 14,
        "graph_stroke_width" : 8,
    }
    def construct(self):
        self.setup_axes()

        cos_graph = self.get_graph(np.cos)
        cos_graph.set_stroke(BLUE, self.graph_stroke_width)
        quad_graph = self.get_graph(taylor_approximation(np.cos, 2))
        quad_graph.set_stroke(GREEN, self.graph_stroke_width)
        quartic = self.get_graph(taylor_approximation(np.cos, 4))
        quartic.set_stroke(PINK, self.graph_stroke_width)
        self.add(cos_graph, quad_graph, quartic)

        title = OldTexText("Taylor Series")
        title.set_width(1.5*FRAME_X_RADIUS)
        title.add_background_rectangle()
        title.to_edge(UP)
        self.add(title)



# ----- From _2017/eoc/footnote.py -----

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


class Thumbnail(SecondDerivativeGraphically):
    CONFIG = {
        "graph_origin" : 5*LEFT + 3*DOWN,
        "x_axis_label" : "",
        "y_axis_label" : "",
    }
    def construct(self):
        self.setup_axes()
        self.force_skipping()
        self.draw_f()
        self.remove(self.graph_label)
        self.graph.set_stroke(GREEN, width = 8)

        tex = OldTex("{d^n f", "\\over", "dx^n}")
        tex.set_color_by_tex("d^n", YELLOW)
        tex.set_color_by_tex("dx", BLUE)
        tex.set_height(4)
        tex.to_edge(UP)

        self.add(tex)
