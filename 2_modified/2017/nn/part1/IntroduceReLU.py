# ==============================================================================
# Scene:      IntroduceReLU
# Source:     videos/_2017/nn/part1.py (lines 4368-4468)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceReLU.py IntroduceReLU -w -m --fps 15
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
import warnings
# CHANGE: Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
import sys, os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # CL17-B
from nn.network import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class IntroduceSigmoid(GraphScene):
    CONFIG = {
        "x_min" : -5,
        "x_max" : 5,
        "x_axis_width" : 12,
        "y_min" : -1,
        "y_max" : 2,
        "y_axis_label" : "",
        "graph_origin" : DOWN,
        "x_labeled_nums" : list(range(-4, 5)),
        "y_labeled_nums" : list(range(-1, 3)),
    }
    def construct(self):
        self.setup_axes()
        self.add_title()
        self.add_graph()
        self.show_part(-5, -2, RED)
        self.show_part(2, 5, GREEN)
        self.show_part(-2, 2, BLUE)

    def add_title(self):
        name = OldTexText("Sigmoid")
        name.next_to(ORIGIN, RIGHT, LARGE_BUFF)
        name.to_edge(UP)
        char = self.x_axis_label.replace("$", "")
        equation = OldTex(
            "\\sigma(%s) = \\frac{1}{1+e^{-%s}}"%(char, char)
        )
        equation.next_to(name, DOWN)
        self.add(equation, name)

        self.equation = equation
        self.sigmoid_name = name

    def add_graph(self):
        graph = self.get_graph(
            lambda x : 1./(1+np.exp(-x)),
            color = YELLOW
        )

        self.play(ShowCreation(graph))
        self.wait()

        self.sigmoid_graph = graph

    ###

    def show_part(self, x_min, x_max, color):
        line, graph_part = [
            self.get_graph(
                func,
                x_min = x_min, 
                x_max = x_max,
                color = color,
            ).set_stroke(width = 4)
            for func in (lambda x : 0, sigmoid)
        ]

        self.play(ShowCreation(line))
        self.wait()
        self.play(Transform(line, graph_part))
        self.wait()


class IntroduceReLU(IntroduceSigmoid):
    CONFIG = {
        "x_axis_label" : "$a$"
    }
    def construct(self):
        self.setup_axes()
        self.add_title()
        self.add_graph()
        self.old_school()
        self.show_ReLU()
        self.label_input_regions()

    def old_school(self):
        sigmoid_graph = self.sigmoid_graph
        sigmoid_title = VGroup(
            self.sigmoid_name,
            self.equation
        )
        cross = Cross(sigmoid_title)
        old_school = OldTexText("Old school")
        old_school.to_corner(UP+RIGHT)
        old_school.set_color(RED)
        arrow = Arrow(
            old_school.get_bottom(), 
            self.equation.get_right(),
            color = RED
        )

        self.play(ShowCreation(cross))
        self.play(
            Write(old_school, run_time = 1),
            GrowArrow(arrow)
        )
        self.wait(2)
        self.play(
            ApplyMethod(
                VGroup(cross, sigmoid_title).shift, 
                FRAME_X_RADIUS*RIGHT,
                rate_func = running_start
            ),
            FadeOut(old_school),
            FadeOut(arrow),
        )
        self.play(ShowCreation(
            self.sigmoid_graph,
            rate_func = lambda t : smooth(1-t),
            remover = True
        ))

    def show_ReLU(self):
        graph = VGroup(
            Line(
                self.coords_to_point(-7, 0),
                self.coords_to_point(0, 0),
            ),
            Line(
                self.coords_to_point(0, 0),
                self.coords_to_point(4, 4),
            ),
        )
        graph.set_color(YELLOW)
        char = self.x_axis_label.replace("$", "")
        equation = OldTexText("ReLU($%s$) = max$(0, %s)$"%(char, char))
        equation.shift(FRAME_X_RADIUS*LEFT/2)
        equation.to_edge(UP)
        equation.add_background_rectangle()
        name = OldTexText("Rectified linear unit")
        name.move_to(equation)
        name.add_background_rectangle()

        self.play(Write(equation))
        self.play(ShowCreation(graph), Animation(equation))
        self.wait(2)
        self.play(
            Write(name),
            equation.shift, DOWN
        )
        self.wait(2)

        self.ReLU_graph = graph

    def label_input_regions(self):
        l1, l2 = self.ReLU_graph
        neg_words = OldTexText("Inactive")
        neg_words.set_color(RED)
        neg_words.next_to(self.coords_to_point(-2, 0), UP)

        pos_words = OldTexText("Same as $f(a) = a$")
        pos_words.set_color(GREEN)
        pos_words.next_to(
            self.coords_to_point(1, 1),
            DOWN+RIGHT
        )

        self.revert_to_original_skipping_status()
        self.play(ShowCreation(l1.copy().set_color(RED)))
        self.play(Write(neg_words))
        self.wait()
        self.play(ShowCreation(l2.copy().set_color(GREEN)))
        self.play(Write(pos_words))
        self.wait(2)
