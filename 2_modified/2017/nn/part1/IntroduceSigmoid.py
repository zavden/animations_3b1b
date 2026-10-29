# ==============================================================================
# Scene:      IntroduceSigmoid
# Source:     videos/_2017/nn/part1.py (lines 2717-2778)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceSigmoid.py IntroduceSigmoid -w -m --fps 15
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
