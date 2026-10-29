# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2017/eoc/chapter3.py (lines 2789-2806)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - smooth/rush_* with `inflection` are the Cairo rate functions (cairo_smooth in cairo_compat)
#   - in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
# ==============================================================================

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



# ----- From _2017/eoc/chapter3.py -----

class NudgeSideLengthOfCube(Scene):
    CONFIG = {
        "x_color" : BLUE,
        "dx_color" : GREEN,
        "df_color" : YELLOW,
        "use_morty" : False,
        "x" : 3,
        "dx" : 0.2,
        "alt_dx" : 0.02,
        "offset_vect" : OUT,
        "pose_angle" : np.pi/12,
        "pose_axis" : UP+RIGHT,
        "small_piece_scaling_factor" : 0.7,
        "allow_recursion" : True,
    }
    def construct(self):
        self.states = dict()
        if self.allow_recursion:
            # CHANGE: in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
            self.alt_scene = cairo_nested_scene(self.__class__,
                skip_animations = True,
                allow_recursion = False,
                dx = self.alt_dx,
            )

        self.add_title()
        self.introduce_cube()
        self.write_df_equation()
        self.write_derivative()

    def add_title(self):
        title = OldTex("f(x) = x^3")
        title.shift(FRAME_X_RADIUS*LEFT/2)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

    def introduce_cube(self):
        cube = self.get_cube()
        cube.to_edge(LEFT, buff = 2*LARGE_BUFF)
        cube.shift(DOWN)

        dv_pieces = self.get_dv_pices(cube)
        original_dx = self.dx
        self.dx = 0
        alt_dv_pieces = self.get_dv_pices(cube)
        self.dx = original_dx
        alt_dv_pieces.set_fill(opacity = 0)

        x_brace = Brace(cube, LEFT, buff = SMALL_BUFF)
        dx_brace = Brace(
            dv_pieces[1], LEFT, buff = SMALL_BUFF,
        )
        dx_brace.stretch_in_place(1.5, 1)
        for brace, tex in (x_brace, "x"), (dx_brace, "dx"):
            brace.scale(0.95)
            brace.rotate(-np.pi/96)
            brace.shift(0.3*(UP+LEFT))
            brace.add(brace.get_text("$%s$"%tex))


        cube_group = VGroup(cube, dv_pieces, alt_dv_pieces)
        self.pose_3d_mobject(cube_group)

        self.play(DrawBorderThenFill(cube))
        self.play(GrowFromCenter(x_brace))
        self.wait()
        self.play(Transform(alt_dv_pieces, dv_pieces))
        self.remove(alt_dv_pieces)
        self.add(dv_pieces)
        self.play(GrowFromCenter(dx_brace))
        self.wait()
        for piece in dv_pieces:
            piece.on_cube_state = piece.copy()
        self.play(*[
            ApplyMethod(
                piece.shift, 
                0.5*(piece.get_center()-cube.get_center())
            )
            for piece in dv_pieces
        ]+[
            ApplyMethod(dx_brace.shift, 0.7*UP)
        ])
        self.wait()

        self.cube = cube
        self.dx_brace = dx_brace
        self.faces, self.bars, self.corner_cube = [
            VGroup(*[
                piece 
                for piece in dv_pieces
                if piece.type == target_type
            ])
            for target_type in ("face", "bar", "corner_cube")
        ]

    def write_df_equation(self):
        df_equation = VGroup(
            OldTex("df"),
            OldTex("="),
            self.organize_faces(self.faces.copy()),
            OldTex("+"),
            self.organize_bars(self.bars.copy()),
            OldTex("+"),
            self.corner_cube.copy()
        )
        df, equals, faces, plus1, bars, plus2, corner_cube = df_equation
        df.set_color(self.df_color)
        for three_d_mob in faces, bars, corner_cube:
            three_d_mob.scale(self.small_piece_scaling_factor)
            # self.pose_3d_mobject(three_d_mob)
        faces.set_fill(opacity = 0.3)
        df_equation.arrange(RIGHT)
        df_equation.next_to(ORIGIN, RIGHT)
        df_equation.to_edge(UP)

        faces_brace = Brace(faces, DOWN)
        derivative = faces_brace.get_tex("3x^2", "\\, dx")
        extras_brace = Brace(VGroup(bars, corner_cube), DOWN)
        ignore_text = extras_brace.get_text(
            "Multiple \\\\ of $dx^2$"
        )
        ignore_text.scale(0.7)
        x_squared_dx = OldTex("x^2", "\\, dx")


        self.play(*list(map(Write, [df, equals])))
        self.grab_pieces(self.faces, faces)
        self.wait()
        self.shrink_dx("Faces are introduced")
        face = self.faces[0]
        face.save_state()
        self.play(face.shift, FRAME_X_RADIUS*RIGHT)
        x_squared_dx.next_to(face, LEFT)
        self.play(Write(x_squared_dx, run_time = 1))
        self.wait()
        for submob, sides in zip(x_squared_dx, [face[0], VGroup(*face[1:])]):
            self.play(
                submob.set_color, RED,
                sides.set_color, RED,
                rate_func = there_and_back
            )
            self.wait()
        self.play(
            face.restore,
            Transform(
                x_squared_dx, derivative,
                replace_mobject_with_target_in_scene = True
            ),
            GrowFromCenter(faces_brace)
        )
        self.wait()
        self.grab_pieces(self.bars, bars, plus1)
        self.grab_pieces(self.corner_cube, corner_cube, plus2)
        self.play(
            GrowFromCenter(extras_brace),
            Write(ignore_text)
        )
        self.wait()
        self.play(*[
            ApplyMethod(mob.fade, 0.7)
            for mob in [
                plus1, bars, plus2, corner_cube, 
                extras_brace, ignore_text
            ]
        ])
        self.wait()

        self.df_equation = df_equation
        self.derivative = derivative

    def write_derivative(self):
        df, equals, faces, plus1, bars, plus2, corner_cube = self.df_equation
        df = df.copy()
        equals = equals.copy()        
        df_equals = VGroup(df, equals)        

        derivative = self.derivative.copy()
        dx = derivative[1]

        extra_stuff = OldTex("+(\\dots)", "dx^2")
        dx_squared = extra_stuff[1]

        derivative.generate_target()
        derivative.target.shift(2*DOWN)
        extra_stuff.next_to(derivative.target)
        self.play(
            MoveToTarget(derivative),
            df_equals.next_to, derivative.target[0], LEFT,
            df_equals.shift, 0.07*DOWN
        )
        self.play(Write(extra_stuff))
        self.wait()

        frac_line = OldTex("-")
        frac_line.replace(df)
        extra_stuff.generate_target()
        extra_stuff.target.next_to(derivative[0])
        frac_line2 = OldTex("-")
        frac_line2.stretch_to_fit_width(
            extra_stuff.target[1].get_width()
        )
        frac_line2.move_to(extra_stuff.target[1])
        extra_stuff.target[1].next_to(frac_line2, UP, buff = SMALL_BUFF)
        dx_below_dx_squared = OldTex("dx")
        dx_below_dx_squared.next_to(frac_line2, DOWN, buff = SMALL_BUFF)
        self.play(
            FadeIn(frac_line),
            FadeIn(frac_line2),
            df.next_to, frac_line, UP, SMALL_BUFF,
            dx.next_to, frac_line, DOWN, SMALL_BUFF,
            MoveToTarget(extra_stuff),
            Write(dx_below_dx_squared),
            path_arc = -np.pi
        )
        self.wait()
        inner_dx = VGroup(*dx_squared[:-1])
        self.play(
            FadeOut(frac_line2),
            FadeOut(dx_below_dx_squared),
            dx_squared[-1].set_color, BLACK,
            inner_dx.next_to, extra_stuff[0], RIGHT, SMALL_BUFF
        )
        self.wait()
        self.shrink_dx("Derivative is written", restore = False)
        self.play(*[
            ApplyMethod(mob.fade, 0.7)
            for mob in (extra_stuff, inner_dx)
        ])
        self.wait(2)

        anims = []
        for mob in list(self.faces)+list(self.bars)+list(self.corner_cube):
            vect = mob.get_center()-self.cube.get_center()
            anims += [
                mob.shift, -(1./3)*vect
            ]
        anims += self.dx_brace.shift, 0.7*DOWN
        self.play(*anims)
        self.wait()

    def grab_pieces(self, start_pieces, end_pices, to_write = None):
        for piece in start_pieces:
            piece.generate_target()
            piece.target.rotate(
                np.pi/12, piece.get_center()-self.cube.get_center()
            )
            piece.target.set_color(RED)
        self.play(*list(map(MoveToTarget, start_pieces)), rate_func = wiggle)
        self.wait()
        added_anims = []
        if to_write is not None:
            added_anims.append(Write(to_write))
        self.play(
            Transform(start_pieces.copy(), end_pices),
            *added_anims
        )

    def shrink_dx(self, state_name, restore = True):
        mobjects = self.get_mobjects()
        mobjects_with_points = [
            m for m in mobjects
            if m.get_num_points() > 0
        ]
        #Alt_scene will reach this point, and save copy of self
        #in states dict
        self.states[state_name] = [
            mob.copy() for mob in mobjects_with_points
        ] 
        if not self.allow_recursion:
            return
        if restore:
            movers = self.states[state_name]
            for mob in movers:
                mob.save_state()
            self.remove(*mobjects)
        else:
            movers = mobjects_with_points
        self.play(*[
            Transform(*pair)
            for pair in zip(
                movers,
                self.alt_scene.states[state_name]
            )
        ])
        self.wait()
        if restore:
            self.play(*[m.restore for m in movers])
            self.remove(*movers)
            self.mobjects = mobjects

    def get_cube(self):
        cube = self.get_prism(self.x, self.x, self.x)
        cube.set_fill(color = BLUE, opacity = 0.3)
        cube.set_stroke(color = WHITE, width = 1)
        return cube

    def get_dv_pices(self, cube):
        pieces = VGroup()
        for vect in it.product([0, 1], [0, 1], [0, 1]):
            if np.all(vect == ORIGIN):
                continue
            args = [
                self.x if bit is 0 else self.dx
                for bit in vect
            ]
            piece = self.get_prism(*args)
            piece.next_to(cube, np.array(vect), buff = 0)
            pieces.add(piece)
            if sum(vect) == 1:
                piece.type = "face"
            elif sum(vect) == 2:
                piece.type = "bar"
            else:
                piece.type = "corner_cube"

        return pieces

    def organize_faces(self, faces):
        self.unpose_3d_mobject(faces)
        for face in faces:
            dimensions = [
                face.length_over_dim(dim)
                for dim in range(3)
            ]
            thin_dim = np.argmin(dimensions)
            if thin_dim == 0:
                face.rotate(np.pi/2, DOWN)
            elif thin_dim == 1:
                face.rotate(np.pi/2, RIGHT)
        faces.arrange(OUT, buff = LARGE_BUFF)
        self.pose_3d_mobject(faces)
        return faces

    def organize_bars(self, bars):
        self.unpose_3d_mobject(bars)
        for bar in bars:
            dimensions = [
                bar.length_over_dim(dim)
                for dim in range(3)
            ]
            thick_dim = np.argmax(dimensions)
            if thick_dim == 0:
                bar.rotate(np.pi/2, OUT)
            elif thick_dim == 2:
                bar.rotate(np.pi/2, LEFT)
        bars.arrange(OUT, buff = LARGE_BUFF)
        self.pose_3d_mobject(bars)
        return bars

    def get_corner_cube(self):
        return self.get_prism(self.dx, self.dx,  self.dx)

    def get_prism(self, width, height, depth):
        color_kwargs = {
            "fill_color" : YELLOW,
            "fill_opacity" : 0.4,
            "stroke_color" : WHITE,            
            "stroke_width" : 0.1,
        }
        front = Rectangle(
            width = width,
            height = height,
            **color_kwargs
        )
        face = VGroup(front)
        for vect in LEFT, RIGHT, UP, DOWN:
            if vect is LEFT or vect is RIGHT:
                side = Rectangle(
                    height = height, 
                    width = depth, 
                    **color_kwargs
                )
            else:
                side = Rectangle(
                    height = depth,
                    width = width, 
                    **color_kwargs
                )
            side.next_to(front, vect, buff = 0)
            side.rotate(
                np.pi/2, rotate_vector(vect, -np.pi/2),
                about_point = front.get_edge_center(vect)
            )
            face.add(side)
        return face

    def pose_3d_mobject(self, mobject):
        mobject.rotate(self.pose_angle, self.pose_axis)
        return mobject

    def unpose_3d_mobject(self, mobject):
        mobject.rotate(-self.pose_angle, self.pose_axis)
        return mobject


class Thumbnail(NudgeSideLengthOfCube):
    def construct(self):
        self.introduce_cube()
        VGroup(*self.get_mobjects()).to_edge(DOWN)

        formula = OldTex(
            "\\frac{d(x^3)}{dx} = 3x^2"
        )
        VGroup(*formula[:5]).set_color(YELLOW)
        VGroup(*formula[-3:]).set_color(GREEN_B)
        formula.set_width(FRAME_X_RADIUS-1)
        formula.to_edge(RIGHT)
        self.add(formula)

        title = OldTexText("Geometric derivatives")
        title.set_width(FRAME_WIDTH-1)
        title.to_edge(UP)
        self.add(title)
