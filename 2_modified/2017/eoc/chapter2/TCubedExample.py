# ==============================================================================
# Scene:      TCubedExample
# Source:     videos/_2017/eoc/chapter2.py (lines 1528-1948)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TCubedExample.py TCubedExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - smooth/rush_* with `inflection` are the Cairo rate functions (cairo_smooth in cairo_compat)
# ==============================================================================

from manim_imports_ext import *

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


class TCubedExample(SecantLineToTangentLine):
    CONFIG = {
        "y_axis_label" : "Distance",
        "y_min" : 0,
        "y_max" : 16,
        "y_tick_frequency" : 1,
        "y_labeled_nums" : list(range(0, 17, 2)),
        "x_min" : 0,
        "x_max" : 4,
        "x_labeled_nums" : list(range(1, 5)),
        "graph_origin" : 2.5*DOWN + 6*LEFT,
        "start_time" : 2,
        "end_time" : 0.5,
        "start_dt" : 0.25,
        "end_dt" : 0.001,
        "secant_line_length" : 0.01,
    }
    def construct(self):
        self.draw_graph()
        self.show_vertical_lines()
        self.bear_with_me()
        self.add_ds_dt_group()
        self.brace_for_details()
        self.show_expansion()
        self.react_to_simplicity()

    def draw_graph(self):
        self.setup_axes(animate = False)
        self.x_axis_label_mob.shift(0.5*DOWN)
        # self.y_axis_label_mob.next_to(self.y_axis, UP)
        graph = self.graph_function(lambda t : t**3, animate = True)
        self.label_graph(
            graph,
            label = "s(t) = t^3",
            proportion = 0.62,
            direction = LEFT,
            buff = SMALL_BUFF
        )
        self.wait()

    def show_vertical_lines(self):
        for t in 1, 2:
            v_line = self.get_vertical_line_to_graph(
                t, line_kwargs = {"color" : WHITE}
            )
            brace = Brace(v_line, RIGHT)
            text = OldTex("%d^3 = %d"%(t, t**3))
            text.next_to(brace, RIGHT)
            text.shift(0.2*UP)
            group = VGroup(v_line, brace, text)
            if t == 1:
                self.play(ShowCreation(v_line))
                self.play(
                    GrowFromCenter(brace),
                    Write(text)
                )
                last_group = group
            else:
                self.play(Transform(last_group, group))
            self.wait()
        self.play(FadeOut(last_group))

    def bear_with_me(self):
        morty = Mortimer()
        morty.to_corner(DOWN+RIGHT)

        self.play(FadeIn(morty))
        self.play(PiCreatureSays(
            morty, "Bear with \\\\ me here",
            target_mode = "sassy"
        ))
        self.play(Blink(morty))
        self.wait()
        self.play(*list(map(
            FadeOut, 
            [morty, morty.bubble, morty.bubble.content]
        )))

    def add_ds_dt_group(self):
        self.curr_time = self.start_time
        self.curr_dt = self.start_dt
        ds_dt_group = self.get_ds_dt_group(dt = self.start_dt)
        v_lines = self.get_vertical_lines()

        lhs = OldTex("\\frac{ds}{dt}(2) = ")
        lhs.next_to(ds_dt_group, UP+RIGHT, buff = MED_LARGE_BUFF)
        ds = VGroup(*lhs[:2])
        dt = VGroup(*lhs[3:5])
        ds.set_color(DISTANCE_COLOR)
        dt.set_color(TIME_COLOR)
        ds.target, dt.target = ds_dt_group[3:5]
        for mob in ds, dt:
            mob.save_state()
            mob.move_to(mob.target)

        nonzero_size = OldTexText("Nonzero size...for now")
        nonzero_size.set_color(TIME_COLOR)
        nonzero_size.next_to(dt, DOWN+2*RIGHT, buff = LARGE_BUFF)
        arrow = Arrow(nonzero_size, dt)

        rhs = OldTex(
            "\\frac{s(2+dt) - s(2)}{dt}"
        )
        rhs.next_to(lhs[-1])
        VGroup(*rhs[4:6]).set_color(TIME_COLOR)
        VGroup(*rhs[-2:]).set_color(TIME_COLOR)
        numerator = VGroup(*rhs[:-3])
        non_numerator = VGroup(*rhs[-3:])
        numerator_non_minus = VGroup(*numerator)
        numerator_non_minus.remove(rhs[7])
        s_pair = rhs[0], rhs[8]
        lp_pair = rhs[6], rhs[11]
        for s, lp in zip(s_pair, lp_pair):
            s.target = OldTex("3").scale(0.7)
            s.target.move_to(lp.get_corner(UP+RIGHT), LEFT)



        self.play(Write(ds_dt_group, run_time = 2))
        self.play(
            FadeIn(lhs),
            *[mob.restore for mob in (ds, dt)]
        )
        self.play(ShowCreation(v_lines[0]))
        self.wait()
        self.play(
            ShowCreation(arrow),
            Write(nonzero_size),
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [arrow, nonzero_size])))
        self.play(Write(numerator))
        self.play(ShowCreation(v_lines[1]))
        self.wait()
        self.play(
            v_lines[0].set_color, YELLOW,
            rate_func = there_and_back
        )
        self.wait()
        self.play(Write(non_numerator))
        self.wait(2)
        self.play(
            *list(map(MoveToTarget, s_pair)),
            **{
                "path_arc" : -np.pi/2
            }
        )
        self.play(numerator_non_minus.shift, 0.2*LEFT)
        self.wait()

        self.vertical_lines = v_lines
        self.ds_dt_group = ds_dt_group
        self.lhs = lhs
        self.rhs = rhs

    def get_vertical_lines(self):
        return VGroup(*[
            self.get_vertical_line_to_graph(
                time,
                line_class = DashedLine,
                line_kwargs = {
                    "color" : WHITE,
                    "dash_length" : 0.05,
                }
            )
            for time in (self.start_time, self.start_time+self.start_dt)
        ])

    def brace_for_details(self):
        morty = Mortimer()
        morty.next_to(self.rhs, DOWN, buff = LARGE_BUFF)

        self.play(FadeIn(morty))
        self.play(
            morty.change_mode, "hooray",
            morty.look_at, self.rhs
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty.change_mode, "sassy",
            morty.look, OUT
        )
        self.play(Blink(morty))
        self.play(morty.change_mode, "pondering")
        self.wait()
        self.play(FadeOut(morty))

    def show_expansion(self):
        expression = OldTex("""
            \\frac{
                2^3 + 
                3 (2)^2 dt
                + 3 (2)(dt)^2 + 
                (dt)^3
                - 2^3
            }{dt}
        """)
        expression.set_width(
            VGroup(self.lhs, self.rhs).get_width()
        )
        expression.next_to(
            self.lhs, DOWN, 
            aligned_edge = LEFT,
            buff = LARGE_BUFF
        )
        term_lens = [
            len("23+"),
            len("3(2)2dt"),
            len("+3(2)(dt)2+"),
            len("(dt)3"),
            len("-23"),
            len("_"),#frac bar
            len("dt"),
        ]
        terms = [
            VGroup(*expression[i1:i2])
            for i1, i2 in zip(
                [0]+list(np.cumsum(term_lens)),
                np.cumsum(term_lens)
            )
        ]

        dts = [
            VGroup(*terms[1][-2:]),
            VGroup(*terms[2][6:8]),
            VGroup(*terms[3][1:3]),
            terms[-1]
        ]
        VGroup(*dts).set_color(TIME_COLOR)

        two_cubed_terms = terms[0], terms[4]

        for term in terms:
            self.play(FadeIn(term))
            self.wait()

        #Cancel out two_cubed terms
        self.play(*it.chain(*[
            [
                tc.scale, 1.3, tc.get_corner(vect),
                tc.set_color, RED
            ]
            for tc, vect in zip(
                two_cubed_terms, 
                [DOWN+RIGHT, DOWN+LEFT]
            )
        ]))
        self.play(*list(map(FadeOut, two_cubed_terms)))
        numerator = VGroup(*terms[1:4])
        self.play(
            numerator.scale, 1.4, numerator.get_bottom(),
            terms[-1].scale, 1.4, terms[-1].get_top()
        )
        self.wait(2)

        #Cancel out dt
        #This is all way too hacky...
        faders = VGroup(
            terms[-1],            
            VGroup(*terms[1][-2:]), #"3(2)^2 dt"
            terms[2][-2], # "+3(2)(dt)2+"
            terms[3][-1], # "(dt)3"
        )
        new_exp = OldTex("2").replace(faders[-1], dim_to_match = 1)
        self.play(
            faders.set_color, BLACK,
            FadeIn(new_exp),
            run_time = 2,
        )
        self.wait()
        terms[3].add(new_exp)
        shift_val = 0.4*DOWN
        self.play(
            FadeOut(terms[-2]),#frac_line
            terms[1].shift, shift_val + 0.45*RIGHT,
            terms[2].shift, shift_val,
            terms[3].shift, shift_val,
        )

        #Isolate dominant term
        arrow = Arrow(
            self.lhs[4].get_bottom(), terms[1][2].get_top(),
            color = WHITE,
            buff = MED_SMALL_BUFF
        )
        brace = Brace(VGroup(terms[2][0], terms[3][-1]), DOWN)
        brace_text = brace.get_text("Contains $dt$")
        VGroup(*brace_text[-2:]).set_color(TIME_COLOR)

        self.play(ShowCreation(arrow))
        self.wait()
        self.play(
            GrowFromCenter(brace), 
            Write(brace_text)
        )
        self.wait(2)

        #Shink dt
        faders = VGroup(*terms[2:4] + [brace, brace_text])        
        def ds_dt_group_update(group, alpha):
            new_dt = interpolate(self.start_dt, self.end_dt, alpha)
            new_group = self.get_ds_dt_group(new_dt)
            Transform(group, new_group).update(1)
        self.play(FadeOut(self.vertical_lines))
        self.secant_line_length = 10
        self.play(Transform(
            self.ds_dt_group,
            self.get_ds_dt_group(self.start_dt)
        ))
        self.play(
            UpdateFromAlphaFunc(self.ds_dt_group, ds_dt_group_update),
            faders.fade, 0.7,
            run_time = 5
        )
        self.wait(2)

        #Show as derivative
        deriv_term = VGroup(*terms[1][:5])
        deriv_term.generate_target()
        lhs_copy = self.lhs.copy()
        lhs_copy.generate_target()
        lhs_copy.target.shift(3*DOWN)
        #hack a little, hack a lot
        deriv_term.target.scale(1.1)
        deriv_term.target.next_to(lhs_copy.target)
        deriv_term.target.shift(0.07*DOWN)

        self.play(
            FadeOut(arrow),
            FadeOut(faders),            
            MoveToTarget(deriv_term),
            MoveToTarget(lhs_copy),
        )
        arrow = Arrow(
            self.rhs.get_bottom(), deriv_term.target.get_top(),
            buff = MED_SMALL_BUFF,
            color = WHITE
        )
        approach_text = OldTexText("As $dt \\to 0$")
        approach_text.next_to(arrow.get_center(), RIGHT)
        VGroup(*approach_text[2:4]).set_color(TIME_COLOR)
        self.play(
            ShowCreation(arrow),
            Write(approach_text)
        )
        self.wait(2)
        self.wait()

        #Ephasize slope
        v_line = self.vertical_lines[0]
        slope_text = OldTexText("Slope = $12$")
        slope_text.set_color(VELOCITY_COLOR)
        slope_text.next_to(v_line.get_end(), LEFT)
        self.play(Write(slope_text))
        self.play(
            self.ds_dt_group.rotate, np.pi/24,
            rate_func = wiggle
        )
        self.play(ShowCreation(v_line))
        self.wait()
        self.play(FadeOut(v_line))
        self.play(FadeOut(slope_text))

        #Generalize to more t
        twos = [
            self.lhs[6],
            self.rhs[2],
            self.rhs[10],
            lhs_copy[6],
            deriv_term[2]
        ]
        for two in twos:
            two.target = OldTex("t")
            two.target.replace(two, dim_to_match = 1)
        self.play(*list(map(MoveToTarget, twos)))
        def update_as_tangent_line(group, alpha):
            self.curr_time = interpolate(self.start_time, self.end_time, alpha)
            new_group = self.get_ds_dt_group(self.end_dt)
            Transform(group, new_group).update(1)
        self.play(
            UpdateFromAlphaFunc(self.ds_dt_group, update_as_tangent_line),
            run_time = 5,
            rate_func = there_and_back
        )
        self.wait(2)

        self.lhs_copy = lhs_copy
        self.deriv_term = deriv_term
        self.approach_text = approach_text

    def react_to_simplicity(self):
        morty = Mortimer().flip().to_corner(DOWN+LEFT)

        self.play(FadeIn(morty))
        self.play(PiCreatureSays(
            morty, "That's \\\\ beautiful!",
            target_mode = "hooray"
        ))
        self.play(Blink(morty))
        self.play(
            morty.change_mode, 'happy',
            *list(map(FadeOut, [morty.bubble, morty.bubble.content]))
        )

        numerator = VGroup(*self.rhs[:12])
        denominator = VGroup(*self.rhs[-2:])
        for mob in numerator, denominator, self.approach_text, self.deriv_term:
            mob.generate_target()
            mob.target.scale(1.2)
            mob.target.set_color(MAROON_B)
            self.play(
                MoveToTarget(
                    mob, rate_func = there_and_back,
                    run_time = 1.5,
                ),
                morty.look_at, mob
            )
            self.wait()
        self.play(Blink(morty))
        self.wait()
