# ==============================================================================
# Scene:      ShowSpeedometer
# Source:     videos/_2017/eoc/chapter2.py (lines 540-610)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowSpeedometer.py ShowSpeedometer -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - smooth/rush_* with `inflection` are the Cairo rate functions (cairo_smooth in cairo_compat)
#   - in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
# ==============================================================================

from manim_imports_ext import *

DISTANCE_COLOR = BLUE


TIME_COLOR = YELLOW


VELOCITY_COLOR = GREEN


class IncrementNumber(Succession):
    CONFIG = {
        "start_num" : 0,
        "changes_per_second" : 1,
        "run_time" : 11,
    }
    def __init__(self, num_mob, **kwargs):
        digest_config(self, kwargs)
        n_iterations = int(self.run_time * self.changes_per_second)
        new_num_mobs = [
            OldTex(str(num)).move_to(num_mob, LEFT)
            for num in range(self.start_num, self.start_num+n_iterations)
        ]
        transforms = [
            Transform(
                num_mob, new_num_mob, 
                run_time = 1.0/self.changes_per_second,
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )
            for new_num_mob in new_num_mobs
        ]
        Succession.__init__(
            self, *transforms, **{
                "rate_func" : None,
                "run_time" : self.run_time,
            }
        )


class IntroduceCar(Scene):
    CONFIG = {
        "should_transition_to_graph" : True,
        "show_distance" : True,
        "point_A" : DOWN+4*LEFT,
        "point_B" : DOWN+5*RIGHT,
    }
    def construct(self):
        point_A, point_B = self.point_A, self.point_B
        A = Dot(point_A)
        B = Dot(point_B)
        line = Line(point_A, point_B)
        VGroup(A, B, line).set_color(WHITE)        
        for dot, tex in (A, "A"), (B, "B"):
            label = OldTex(tex).next_to(dot, DOWN)
            dot.add(label)

        car = Car()
        self.car = car #For introduce_added_mobjects use in subclasses
        car.move_to(point_A)
        front_line = car.get_front_line()

        time_label = OldTexText("Time (in seconds):", "0")
        time_label.shift(2*UP)

        distance_brace = Brace(line, UP)
        # distance_brace.set_fill(opacity = 0.5)
        distance = distance_brace.get_text("100m")

        self.add(A, B, line, car, time_label)
        self.play(ShowCreation(front_line))
        self.play(FadeOut(front_line))
        self.introduce_added_mobjects()
        self.play(
            MoveCar(car, point_B, run_time = 10),
            IncrementNumber(time_label[1], run_time = 11),
            *self.get_added_movement_anims()
        )
        front_line = car.get_front_line()
        self.play(ShowCreation(front_line))
        self.play(FadeOut(front_line))

        if self.show_distance:
            self.play(
                GrowFromCenter(distance_brace),
                Write(distance)
            )
            self.wait()

        if self.should_transition_to_graph:
            self.play(
                car.move_to, point_A,
                FadeOut(time_label),
                FadeOut(distance_brace),
                FadeOut(distance),
            )
            # CHANGE: in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
            graph_scene = cairo_nested_scene(GraphCarTrajectory,skip_animations = True)
            origin = graph_scene.graph_origin
            top = graph_scene.coords_to_point(0, 100)
            new_length = get_norm(top-origin)
            new_point_B = point_A + new_length*RIGHT
            car_line_group = VGroup(car, A, B, line)
            for mob in car_line_group:
                mob.generate_target()
            car_line_group.target = VGroup(*[
                m.target for m in car_line_group
            ])
            B = car_line_group[2]
            B.target.shift(new_point_B - point_B)
            line.target.put_start_and_end_on(
                point_A, new_point_B
            )

            car_line_group.target.rotate(np.pi/2, about_point = point_A)
            car_line_group.target.shift(graph_scene.graph_origin - point_A)
            self.play(MoveToTarget(car_line_group, path_arc = np.pi/2))
            self.wait()

    def introduce_added_mobjects(self):
        pass

    def get_added_movement_anims(self):
        return []


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


class ShowSpeedometer(IntroduceCar):
    CONFIG = {
        "num_ticks" : 8,
        "tick_length" : 0.2,
        "needle_width" : 0.1,
        "needle_height" : 0.8,
        "should_transition_to_graph" : False,
        "show_distance" : False,
        "speedometer_title_text" : "Speedometer",
    }
    def setup(self):
        start_angle = -np.pi/6
        end_angle = 7*np.pi/6
        speedometer = Arc(
            start_angle = start_angle,
            angle = end_angle-start_angle
        )
        tick_angle_range = np.linspace(end_angle, start_angle, self.num_ticks)
        for index, angle in enumerate(tick_angle_range):
            vect = rotate_vector(RIGHT, angle)
            tick = Line((1-self.tick_length)*vect, vect)
            label = OldTex(str(10*index))
            label.set_height(self.tick_length)
            label.shift((1+self.tick_length)*vect)
            speedometer.add(tick, label)

        needle = Polygon(
            LEFT, UP, RIGHT,
            stroke_width = 0,
            fill_opacity = 1,
            fill_color = YELLOW
        )
        needle.stretch_to_fit_width(self.needle_width)
        needle.stretch_to_fit_height(self.needle_height)
        needle.rotate(end_angle-np.pi/2)
        speedometer.add(needle)
        speedometer.needle = needle

        speedometer.center_offset = speedometer.get_center()

        speedometer_title = OldTexText(self.speedometer_title_text)
        speedometer_title.to_corner(UP+LEFT)
        speedometer.next_to(speedometer_title, DOWN)

        self.speedometer = speedometer
        self.speedometer_title = speedometer_title

    def introduce_added_mobjects(self):
        speedometer = self.speedometer
        speedometer_title = self.speedometer_title

        speedometer.save_state()
        speedometer.rotate(-np.pi/2, UP)
        speedometer.set_height(self.car.get_height()/4)
        speedometer.move_to(self.car)
        speedometer.shift((self.car.get_width()/4)*RIGHT)

        self.play(speedometer.restore, run_time = 2)
        self.play(Write(speedometer_title, run_time = 1))

    def get_added_movement_anims(self, **kwargs):
        needle = self.speedometer.needle
        center = self.speedometer.get_center() - self.speedometer.center_offset
        default_kwargs = {
            "about_point" : center,
            "radians" : -np.pi/2,
            "run_time" : 10,
            "rate_func" : there_and_back,
        }
        default_kwargs.update(kwargs)
        return [Rotating(needle, **default_kwargs)]
