# ==============================================================================
# Scene:      VelocityAtIndividualPointsVsPairs
# Source:     videos/_2017/eoc/chapter2.py (lines 788-878)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl VelocityAtIndividualPointsVsPairs.py VelocityAtIndividualPointsVsPairs -w -m --fps 15
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


class VelocityAtIndividualPointsVsPairs(GraphCarTrajectory):
    CONFIG = {
        "start_time" : 6.5,
        "end_time" : 3,
        "dt" : 1.0,
    }
    def construct(self):
        self.setup_axes(animate = False)
        distance_graph = self.graph_function(lambda t : 100*smooth(t/10.))
        distance_label = self.label_graph(
            distance_graph,
            label = "s(t)",
            proportion = 1,
            direction = RIGHT,
            buff = SMALL_BUFF
        )
        velocity_graph = self.get_derivative_graph()
        self.play(ShowCreation(velocity_graph))
        velocity_label = self.label_graph(
            velocity_graph, 
            label = "v(t)",
            proportion = self.start_time/10.0, 
            direction = UP,
            buff = MED_SMALL_BUFF
        )
        velocity_graph.add(velocity_label)

        self.show_individual_times_to_velocity(velocity_graph)
        self.play(velocity_graph.fade, 0.4)
        self.show_two_times_on_distance()
        self.show_confused_pi_creature()

    def show_individual_times_to_velocity(self, velocity_graph):
        start_time = self.start_time
        end_time = self.end_time
        line = self.get_vertical_line_to_graph(start_time, velocity_graph)
        def line_update(line, alpha):
            time = interpolate(start_time, end_time, alpha)
            line.put_start_and_end_on(
                self.coords_to_point(time, 0),
                self.input_to_graph_point(time, graph = velocity_graph)
            )

        self.play(ShowCreation(line))
        self.wait()
        self.play(UpdateFromAlphaFunc(
            line, line_update,
            run_time = 4,
            rate_func = there_and_back
        ))
        self.wait()
        velocity_graph.add(line)

    def show_two_times_on_distance(self):
        line1 = self.get_vertical_line_to_graph(self.start_time-self.dt/2.0)
        line2 = self.get_vertical_line_to_graph(self.start_time+self.dt/2.0)
        p1 = line1.get_end()
        p2 = line2.get_end()
        interim_point = p2[0]*RIGHT+p1[1]*UP
        dt_line = Line(p1, interim_point, color = TIME_COLOR)
        ds_line = Line(interim_point, p2, color = DISTANCE_COLOR)
        dt_brace = Brace(dt_line, DOWN, buff = SMALL_BUFF)
        ds_brace = Brace(ds_line, RIGHT, buff = SMALL_BUFF)
        dt_text = dt_brace.get_text("Change in time", buff = SMALL_BUFF)
        ds_text = ds_brace.get_text("Change in distance", buff = SMALL_BUFF)

        self.play(ShowCreation(VGroup(line1, line2)))
        for line, brace, text in (dt_line, dt_brace, dt_text), (ds_line, ds_brace, ds_text):
            brace.set_color(line.get_color())
            text.set_color(line.get_color())
            text.add_background_rectangle()
            self.play(
                ShowCreation(line),
                GrowFromCenter(brace),
                Write(text)
            )
            self.wait()

    def show_confused_pi_creature(self):
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)
        randy.shift(2*RIGHT)

        self.play(randy.change_mode, "confused")
        self.play(Blink(randy))
        self.wait(2)
        self.play(Blink(randy))
        self.play(randy.change_mode, "erm")
        self.wait()
        self.play(Blink(randy))
        self.wait(2)
