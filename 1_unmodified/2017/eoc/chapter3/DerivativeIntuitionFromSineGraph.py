# ==============================================================================
# Scene:      DerivativeIntuitionFromSineGraph
# Source:     videos/_2017/eoc/chapter3.py (lines 2334-2462)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl DerivativeIntuitionFromSineGraph.py DerivativeIntuitionFromSineGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter3.py -----

DERIVATIVE_COLOR = VELOCITY_COLOR


class IntroduceUnitCircleWithSine(GraphScene):
    CONFIG = {
        "unit_length" : 2.5,
        "graph_origin" : ORIGIN,
        "x_axis_width" : 15,
        "y_axis_height" : 10,
        "x_min" : -3,
        "x_max" : 3,
        "y_min" : -2,
        "y_max" : 2,
        "x_labeled_nums" : [-2, -1, 1, 2],
        "y_labeled_nums" : [-1, 1],
        "x_tick_frequency" : 0.5,
        "y_tick_frequency" : 0.5,
        "circle_color" : BLUE,
        "example_radians" : 0.8,
        "rotations_per_second" : 0.25,
        "include_radial_line_dot" : True,
        "remove_angle_label" : True,
        "line_class" : DashedLine,
        "theta_label" : "= 0.8",
    }
    def construct(self):
        self.setup_axes()
        self.add_title()
        self.introduce_unit_circle()
        self.draw_example_radians()
        self.label_sine()
        self.walk_around_circle()

    def add_title(self):
        title = OldTex("f(\\theta) = \\sin(\\theta)")
        title.to_corner(UP+LEFT)
        self.add(title)
        self.title = title

    def introduce_unit_circle(self):
        circle = self.get_unit_circle()
        radial_line = Line(ORIGIN, self.unit_length*RIGHT)
        radial_line.set_color(RED)
        if self.include_radial_line_dot:
            dot = Dot()
            dot.move_to(radial_line.get_end())
            radial_line.add(dot)

        self.play(ShowCreation(radial_line))
        self.play(
            ShowCreation(circle),            
            Rotate(radial_line, 2*np.pi),
            run_time = 2,
        )
        self.wait()

        self.circle = circle
        self.radial_line = radial_line

    def draw_example_radians(self):
        circle = self.circle
        radial_line = self.radial_line

        line = Line(
            ORIGIN, self.example_radians*self.unit_length*UP,
            color = YELLOW,
        )
        line.shift(FRAME_X_RADIUS*RIGHT/3).to_edge(UP)
        line.insert_n_curves(10)
        line.make_smooth()

        arc = Arc(
            self.example_radians, radius = self.unit_length,
            color = line.get_color(),
        )
        arc_copy = arc.copy().set_color(WHITE)

        brace = Brace(line, RIGHT)
        brace_text = brace.get_text("$\\theta%s$"%self.theta_label)
        brace_text.set_color(line.get_color())
        theta_copy = brace_text[0].copy()

        self.play(
            GrowFromCenter(line),
            GrowFromCenter(brace),
        )
        self.play(Write(brace_text))
        self.wait()
        self.play(
            line.move_to, radial_line.get_end(), DOWN,
            FadeOut(brace)
        )
        self.play(ReplacementTransform(line, arc))
        self.wait()
        self.play(
            Rotate(radial_line, self.example_radians),
            ShowCreation(arc_copy)
        )
        self.wait()
        arc_copy.generate_target()
        arc_copy.target.scale(0.2)
        theta_copy.generate_target()
        theta_copy.target.next_to(
            arc_copy.target, RIGHT,
            aligned_edge = DOWN,
            buff = SMALL_BUFF
        )
        theta_copy.target.shift(SMALL_BUFF*UP)
        self.play(*list(map(MoveToTarget, [arc_copy, theta_copy])))
        self.wait()

        self.angle_label = VGroup(arc_copy, theta_copy)
        self.example_theta_equation = brace_text

    def label_sine(self):
        radial_line = self.radial_line

        drop_point = radial_line.get_end()[0]*RIGHT
        v_line = self.line_class(radial_line.get_end(), drop_point)
        brace = Brace(v_line, RIGHT)
        brace_text = brace.get_text("$\\sin(\\theta)$")
        brace_text[-2].set_color(YELLOW)

        self.play(ShowCreation(v_line))
        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        self.wait()
        faders = [brace, brace_text, self.example_theta_equation]
        if self.remove_angle_label:
            faders += self.angle_label
        self.play(*list(map(FadeOut, faders)))

        self.v_line = v_line

    def walk_around_circle(self):
        radial_line = self.radial_line
        v_line = self.v_line

        def v_line_update(v_line):
            drop_point = radial_line.get_end()[0]*RIGHT
            v_line.put_start_and_end_on(
                radial_line.get_end(), drop_point
            )
            return v_line
        filler_arc = self.circle.copy()
        filler_arc.set_color(YELLOW)
        curr_arc_portion = self.example_radians/(2*np.pi)
        filler_portion = 1 - curr_arc_portion
        filler_arc.pointwise_become_partial(filler_arc, curr_arc_portion, 1)

        self.play(
            Rotate(radial_line, filler_portion*2*np.pi),
            ShowCreation(filler_arc),
            UpdateFromFunc(v_line, v_line_update),
            run_time = filler_portion/self.rotations_per_second,
            rate_func=linear,
        )
        for x in range(5):
            self.play(
                Rotate(radial_line, 2*np.pi),
                UpdateFromFunc(v_line, v_line_update),
                run_time = 1./self.rotations_per_second,
                rate_func=linear,
            )

    ##############

    def setup_axes(self):
        GraphScene.setup_axes(self)
        VGroup(*self.x_axis.numbers[:2]).shift(MED_SMALL_BUFF*LEFT)
        VGroup(*self.x_axis.numbers[2:]).shift(SMALL_BUFF*RIGHT)
        self.y_axis.numbers[0].shift(MED_SMALL_BUFF*DOWN)
        self.y_axis.numbers[1].shift(MED_SMALL_BUFF*UP)

    def get_unit_circle(self):
        return Circle(
            radius = self.unit_length,
            color = self.circle_color,
        )


class DerivativeIntuitionFromSineGraph(GraphScene):
    CONFIG = {
        "graph_origin" : 6*LEFT,
        "x_axis_width" : 11,
        "x_min" : 0,
        "x_max" : 4*np.pi,
        "x_labeled_nums" : np.arange(0, 4*np.pi, np.pi),
        "x_tick_frequency" : np.pi/4,
        "x_axis_label" : "$\\theta$",
        "y_axis_height" : 6,
        "y_min" : -2,
        "y_max" : 2,
        "y_tick_frequency" : 0.5,
        "y_axis_label" : "",
    }
    def construct(self):
        self.setup_axes()
        self.draw_sine_graph()
        self.draw_derivative_from_slopes()
        self.alter_derivative_graph()

    def draw_sine_graph(self):
        graph = self.get_graph(np.sin)
        v_line = DashedLine(ORIGIN, UP)
        rps = IntroduceUnitCircleWithSine.CONFIG["rotations_per_second"]
        self.play(
            ShowCreation(graph),
            UpdateFromFunc(v_line, lambda v : self.v_line_update(v, graph)),
            run_time = 2./rps,
            rate_func=linear
        )
        self.wait()
        self.graph = graph

    def draw_derivative_from_slopes(self):
        ss_group = self.get_secant_slope_group(
            0, self.graph,
            dx = 0.01,
            secant_line_color = RED,
        )
        deriv_graph = self.get_graph(np.cos, color = DERIVATIVE_COLOR)
        v_line = DashedLine(
            self.graph_origin, self.coords_to_point(0, 1), 
            color = RED
        )

        self.play(ShowCreation(ss_group, lag_ratio = 0))
        self.play(ShowCreation(v_line))
        self.wait()
        last_theta = 0
        next_theta = np.pi/2
        while last_theta < self.x_max:
            deriv_copy = deriv_graph.copy()
            self.animate_secant_slope_group_change(
                ss_group,
                target_x = next_theta,
                added_anims = [
                    ShowCreation(
                        deriv_copy,
                        rate_func = lambda t : interpolate(
                            last_theta/self.x_max, 
                            next_theta/self.x_max,
                            smooth(t)
                        ),
                        run_time = 3,
                    ),
                    UpdateFromFunc(
                        v_line, 
                        lambda v : self.v_line_update(v, deriv_copy),
                        run_time = 3
                    ),
                ]
            )
            self.wait()
            if next_theta == 2*np.pi:
                words = OldTexText("Looks a lot like $\\cos(\\theta)$")
                words.next_to(self.graph_origin, RIGHT)
                words.to_edge(UP)
                arrow = Arrow(
                    words.get_bottom(), 
                    deriv_graph.point_from_proportion(0.45)
                )
                VGroup(words, arrow).set_color(deriv_graph.get_color())
                self.play(
                    Write(words),
                    ShowCreation(arrow)
                )
            self.remove(deriv_copy)
            last_theta = next_theta
            next_theta += np.pi/2
        self.add(deriv_copy)

        self.deriv_graph = deriv_copy

    def alter_derivative_graph(self):
        func_list = [
            lambda x : 0.5*(np.cos(x)**3 + np.cos(x)),
            lambda x : 0.75*(np.sign(np.cos(x))*np.cos(x)**2 + np.cos(x)),
            lambda x : 2*np.cos(x),
            lambda x : np.cos(x),
        ]
        for func in func_list:
            new_graph = self.get_graph(func, color = DERIVATIVE_COLOR)
            self.play(
                Transform(self.deriv_graph, new_graph),
                run_time = 2
            )
            self.wait()

    ######

    def v_line_update(self, v_line, graph):
        point = graph.point_from_proportion(1)
        drop_point = point[0]*RIGHT
        v_line.put_start_and_end_on(drop_point, point)
        return v_line

    def setup_axes(self):
        GraphScene.setup_axes(self)
        self.x_axis.remove(self.x_axis.numbers)
        self.remove(self.x_axis.numbers)
        for x in range(1, 4):
            if x == 1:
                label = OldTex("\\pi")
            else:
                label = OldTex("%d\\pi"%x)
            label.next_to(self.coords_to_point(x*np.pi, 0), DOWN, MED_LARGE_BUFF)
            self.add(label)
        self.x_axis_label_mob.set_color(YELLOW)
