# ==============================================================================
# Scene:      CompareLearningCurves
# Source:     videos/_2017/nn/part2.py (lines 3616-3687)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py
#
# Run from this folder:
#     manimgl CompareLearningCurves.py CompareLearningCurves -w -m --fps 15
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


# ----- From _2017/nn/network.py -----

#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))


def ReLU(z):
    result = np.array(z)
    result[result < 0] = 0
    return result



# ----- From _2017/nn/part1.py -----

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2017/nn/part2.py -----

class CompareLearningCurves(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "y_axis_label" : "Value of \\\\ cost function",
        "x_axis_label" : "Number of gradient \\\\ descent steps",
        "graph_origin" : 2*DOWN + 3.5*LEFT,
    }
    def construct(self):
        self.setup_axes()
        self.x_axis_label_mob.to_edge(DOWN)
        self.y_axis_label_mob.to_edge(LEFT)
        self.y_axis_label_mob.set_color(RED)

        slow_decrease = self.get_graph(
            lambda x : 9 - 0.25*x
        )
        faster_decrease = self.get_graph(
            lambda x : 4.3*sigmoid(5*(2-x)) + 3 + 0.5*ReLU(3-x)
        )
        for decrease, p in (slow_decrease, 0.2), (faster_decrease, 0.07):
            y_vals = decrease.get_anchors()[:,1]
            y_vals -= np.cumsum(p*np.random.random(len(y_vals)))
            decrease.make_jagged()
        faster_decrease.move_to(slow_decrease, UP+LEFT)

        slow_label = OldTexText("Randomly-labeled data")
        slow_label.set_color(slow_decrease.get_color())
        slow_label.to_corner(UP+RIGHT)
        slow_line = Line(ORIGIN, RIGHT)
        slow_line.set_stroke(slow_decrease.get_color(), 5)
        slow_line.next_to(slow_label, LEFT)

        fast_label = OldTexText("Properly-labeled data")
        fast_label.set_color(faster_decrease.get_color())
        fast_label.next_to(slow_label, DOWN)
        fast_line = slow_line.copy()
        fast_line.set_color(faster_decrease.get_color())
        fast_line.next_to(fast_label, LEFT)

        self.play(FadeIn(slow_label), ShowCreation(slow_line))
        self.play(ShowCreation(
            slow_decrease,
            run_time = 12,
            rate_func=linear,
        ))
        self.play(FadeIn(fast_label), ShowCreation(fast_line))
        self.play(ShowCreation(
            faster_decrease,
            run_time = 12,
            rate_func=linear,
        ))
        self.wait()

        ####

        line = Line(
            self.coords_to_point(1, 2),
            self.coords_to_point(3, 9),
        )
        rect = Rectangle()
        rect.set_fill(YELLOW, 0.3)
        rect.set_stroke(width = 0)
        rect.replace(line, stretch = True)

        words = OldTexText("Learns structured data more quickly")
        words.set_color(YELLOW)
        words.next_to(rect, DOWN)
        words.add_background_rectangle()

        self.play(DrawBorderThenFill(rect))
        self.play(Write(words))
        self.wait()
