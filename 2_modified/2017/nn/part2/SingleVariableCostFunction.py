# ==============================================================================
# Scene:      SingleVariableCostFunction
# Source:     videos/_2017/nn/part2.py (lines 1440-1808)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl SingleVariableCostFunction.py SingleVariableCostFunction -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

import sys
import os.path
from manim_imports_ext import *
#### Libraries
# Standard library
import os
# Third-party libraries
import numpy as np
import warnings
# CHANGE: Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
import sys, os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # CL17-B
from nn.network import *


# ----- From _2017/nn/part1.py -----

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2017/nn/part2.py -----

class SingleVariableCostFunction(GraphScene):
    CONFIG = {
        "x_axis_label" : "$w$",
        "y_axis_label" : "",
        "x_min" : -5,
        "x_max" : 7,
        "x_axis_width" : 12,
        "graph_origin" : 2.5*DOWN + LEFT,
        "tangent_line_color" : YELLOW,
    }
    def construct(self):
        self.reduce_full_function_to_single_variable()
        self.show_graph()
        self.find_exact_solution()
        self.make_function_more_complicated()
        self.take_steps()
        self.take_steps_based_on_slope()
        self.ball_rolling_down_hill()
        self.note_step_sizes()

    def reduce_full_function_to_single_variable(self):
        name = OldTexText("Cost function")
        cf1 = OldTex("C(", "w_1, w_2, \\dots, w_{13{,}002}", ")")
        cf2 = OldTex("C(", "w", ")")
        for cf in cf1, cf2:
            VGroup(cf[0], cf[2]).set_color(RED)
        big_brace, lil_brace = [
            Brace(cf[1], DOWN)
            for cf in (cf1, cf2)
        ]
        big_brace_text = big_brace.get_text("Weights and biases")
        lil_brace_text = lil_brace.get_text("Single input")

        name.next_to(cf1, UP, LARGE_BUFF)
        name.set_color(RED)

        self.add(name, cf1)
        self.play(
            GrowFromCenter(big_brace),
            FadeIn(big_brace_text)
        )
        self.wait()
        self.play(
            ReplacementTransform(big_brace, lil_brace),
            ReplacementTransform(big_brace_text, lil_brace_text),
            ReplacementTransform(cf1, cf2),
        )

        # cf2.add_background_rectangle()
        lil_brace_text.add_background_rectangle()
        self.brace_group = VGroup(lil_brace, lil_brace_text)
        cf2.add(self.brace_group)
        self.function_label = cf2
        self.to_fade = name

    def show_graph(self):
        function_label = self.function_label
        self.setup_axes()
        graph = self.get_graph(
            lambda x : 0.5*(x - 3)**2 + 2,
            color = RED
        )

        self.play(
            FadeOut(self.to_fade),
            Write(self.axes),
            Animation(function_label),
            run_time = 1,
        )
        self.play(
            function_label.next_to, 
                self.input_to_graph_point(5, graph), RIGHT,
            ShowCreation(graph)
        )
        self.wait()

        self.graph = graph

    def find_exact_solution(self):
        function_label = self.function_label
        graph = self.graph

        w_min = OldTex("w", "_{\\text{min}}", arg_separator = "")
        w_min.move_to(function_label[1], UP+LEFT)
        w_min[1].fade(1)
        x = 3
        dot = Dot(
            self.input_to_graph_point(x, graph),
            color = YELLOW
        )
        line = self.get_vertical_line_to_graph(
            x, graph, 
            line_class = DashedLine,
            color = YELLOW
        )
        formula = OldTex("\\frac{dC}{dw}(w) = 0")
        formula.next_to(dot, UP, buff = 2)
        formula.shift(LEFT)
        arrow = Arrow(formula.get_bottom(), dot.get_center())

        self.play(
            w_min.shift, 
                line.get_bottom() - w_min[0].get_top(),
                MED_SMALL_BUFF*DOWN,
            w_min.set_fill, WHITE, 1,
        )
        self.play(ShowCreation(line))
        self.play(DrawBorderThenFill(dot, run_time = 1))
        self.wait()
        self.play(Write(formula, run_time = 2))
        self.play(GrowArrow(arrow))
        self.wait()

        self.dot = dot
        self.line = line
        self.w_min = w_min
        self.deriv_group = VGroup(formula, arrow)

    def make_function_more_complicated(self):
        dot = self.dot
        line = self.line
        w_min = self.w_min
        deriv_group = self.deriv_group
        function_label = self.function_label
        brace_group = function_label[-1]
        function_label.remove(brace_group)

        brace = Brace(deriv_group, UP)
        words = OldTexText("Sometimes \\\\ infeasible")
        words.next_to(deriv_group, UP)
        words.set_color(BLUE)
        words.next_to(brace, UP)

        graph = self.get_graph(
            lambda x : 0.05*((x+2)*(x-1)*(x-3))**2 + 2 + 0.3*(x-3),
            color = RED
        )

        self.play(
            ReplacementTransform(self.graph, graph),
            function_label.shift, 2*UP+1.9*LEFT,
            FadeOut(brace_group),
            Animation(dot)
        )
        self.graph = graph
        self.play(
            Write(words, run_time = 1),
            GrowFromCenter(brace)
        )
        self.wait(2)
        self.play(FadeOut(VGroup(words, brace, deriv_group)))

    def take_steps(self):
        dot = self.dot
        line = self.line
        w_mob, min_mob = self.w_min
        graph = self.graph

        def update_line(line):
            x = self.x_axis.point_to_number(w_mob.get_center())
            line.put_start_and_end_on_with_projection(
                self.coords_to_point(x, 0),
                self.input_to_graph_point(x, graph)
            )
            return line
        line_update_anim = UpdateFromFunc(line, update_line)

        def update_dot(dot):
            dot.move_to(line.get_end())
            return dot
        dot_update_anim = UpdateFromFunc(dot, update_dot)

        point = self.coords_to_point(2, 0)
        arrows = VGroup()
        q_marks = VGroup()
        for vect, color in (LEFT, BLUE), (RIGHT, GREEN):
            arrow = Arrow(ORIGIN, vect, buff = SMALL_BUFF)
            arrow.shift(point + SMALL_BUFF*UP)
            arrow.set_color(color)
            arrows.add(arrow)
            q_mark = OldTexText("?")
            q_mark.next_to(arrow, UP, buff = 0)
            q_mark.add_background_rectangle()
            q_marks.add(q_mark)

        self.play(
            w_mob.next_to, point, DOWN,
            FadeOut(min_mob),
            line_update_anim, 
            dot_update_anim,
        )
        self.wait()
        self.play(*it.chain(
            list(map(GrowArrow, arrows)),
            list(map(FadeIn, q_marks)),
        ))
        self.wait()

        self.arrow_group = VGroup(arrows, q_marks)
        self.line_update_anim = line_update_anim
        self.dot_update_anim = dot_update_anim
        self.w_mob = w_mob

    def take_steps_based_on_slope(self):
        arrows, q_marks = arrow_group = self.arrow_group
        line_update_anim = self.line_update_anim
        dot_update_anim = self.dot_update_anim
        dot = self.dot
        w_mob = self.w_mob
        graph = self.graph

        x = self.x_axis.point_to_number(w_mob.get_center())
        tangent_line = self.get_tangent_line(x, arrows[0].get_color())

        self.play(
            ShowCreation(tangent_line),
            Animation(dot),
        )
        self.play(VGroup(arrows[1], q_marks).set_fill, None, 0)
        self.play(
            w_mob.shift, MED_SMALL_BUFF*LEFT,
            MaintainPositionRelativeTo(arrow_group, w_mob),
            line_update_anim, dot_update_anim,
        )
        self.wait()

        new_x = 0.3
        new_point = self.coords_to_point(new_x, 0)
        new_tangent_line = self.get_tangent_line(
            new_x, arrows[1].get_color()
        )
        self.play(
            FadeOut(tangent_line),
            w_mob.next_to, new_point, DOWN,
            arrow_group.next_to, new_point, UP, SMALL_BUFF,
            arrow_group.set_fill, None, 1,
            dot_update_anim,
            line_update_anim,
        )
        self.play(
            ShowCreation(new_tangent_line),
            Animation(dot),
            Animation(arrow_group),
        )
        self.wait()
        self.play(VGroup(arrows[0], q_marks).set_fill, None, 0)
        self.play(
            w_mob.shift, MED_SMALL_BUFF*RIGHT,
            MaintainPositionRelativeTo(arrow_group, w_mob),
            line_update_anim, dot_update_anim,
        )
        self.play(
            FadeOut(VGroup(new_tangent_line, arrow_group)),
            Animation(dot),
        )
        self.wait()
        for x in 0.8, 1.1, 0.95:
            self.play(
                w_mob.next_to, self.coords_to_point(x, 0), DOWN,
                line_update_anim,
                dot_update_anim,
            )
        self.wait()

    def ball_rolling_down_hill(self):
        ball = self.dot
        graph = self.graph
        point = VectorizedPoint(self.coords_to_point(-0.5, 0))
        w_mob = self.w_mob

        def update_ball(ball):
            x = self.x_axis.point_to_number(ball.point.get_center())
            graph_point = self.input_to_graph_point(x, graph)
            vect = rotate_vector(UP, self.angle_of_tangent(x, graph))
            radius = ball.get_width()/2
            ball.move_to(graph_point + radius*vect)
            return ball

        def update_point(point, dt):
            x = self.x_axis.point_to_number(point.get_center())
            slope = self.slope_of_tangent(x, graph)
            if abs(slope) > 0.5:
                slope = 0.5 * slope / abs(slope)
            x -= slope*dt
            point.move_to(self.coords_to_point(x, 0))


        ball.generate_target()
        ball.target.scale(2)
        ball.target.set_fill(opacity = 0)
        ball.target.set_stroke(BLUE, 3)
        ball.point = point
        ball.target.point = point
        update_ball(ball.target)

        self.play(MoveToTarget(ball))
        self.play(
            point.move_to, w_mob,
            UpdateFromFunc(ball, update_ball),
            run_time = 3,
        )
        self.wait(2)

        points = [
            VectorizedPoint(self.coords_to_point(x, 0))
            for x in np.linspace(-2.7, 3.7, 11)
        ]
        balls = VGroup()
        updates = []
        for point in points:
            new_ball = ball.copy() 
            new_ball.point = point
            balls.add(new_ball)
            updates += [
                Mobject.add_updater(point, update_point),
                Mobject.add_updater(new_ball, update_ball)
            ]
        balls.set_color_by_gradient(BLUE, GREEN)

        self.play(ReplacementTransform(ball, balls))
        self.add(*updates)
        self.wait(5)
        self.remove(*updates)
        self.remove(*points)
        self.play(FadeOut(balls))

    def note_step_sizes(self):
        w_mob = self.w_mob
        line_update_anim = self.line_update_anim

        x = -0.5
        target_x = 0.94
        point = VectorizedPoint(self.coords_to_point(x, 0))
        line = self.get_tangent_line(x)
        line.scale(0.5)
        def update_line(line):
            x = self.x_axis.point_to_number(point.get_center())
            self.make_line_tangent(line, x)
            return line

        self.play(
            ShowCreation(line),
            w_mob.next_to, point, DOWN,
            line_update_anim,
        )
        for n in range(6):
            x = self.x_axis.point_to_number(point.get_center())
            new_x = interpolate(x, target_x, 0.5)
            self.play(
                point.move_to, self.coords_to_point(new_x, 0),
                MaintainPositionRelativeTo(w_mob, point),
                line_update_anim,
                UpdateFromFunc(line, update_line),
            )
            self.wait(0.5)
        self.wait()

    ###

    def get_tangent_line(self, x, color = YELLOW):
        tangent_line = Line(LEFT, RIGHT).scale(3)
        tangent_line.set_color(color)
        self.make_line_tangent(tangent_line, x)
        return tangent_line

    def make_line_tangent(self, line, x):
        graph = self.graph
        line.rotate(self.angle_of_tangent(x, graph) - line.get_angle())
        line.move_to(self.input_to_graph_point(x, graph))
