# ==============================================================================
# Scene:      FunctionMinmization
# Source:     videos/_2017/nn/part2.py (lines 541-574)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl FunctionMinmization.py FunctionMinmization -w -m --fps 15
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

class FunctionMinmization(GraphScene):
    CONFIG = {
        "x_labeled_nums" : list(range(-1, 10)),
    }
    def construct(self):
        self.setup_axes()
        title = OldTexText("Finding minima")
        title.to_edge(UP)
        self.add(title)

        def func(x):
            x -= 4.5
            return 0.03*(x**4 - 16*x**2) + 0.3*x + 4
        graph = self.get_graph(func)
        graph_label = self.get_graph_label(graph, "C(x)")
        self.add(graph, graph_label)

        dots = VGroup(*[
            Dot().move_to(self.input_to_graph_point(x, graph))
            for x in range(10)
        ])
        dots.set_color_by_gradient(YELLOW, RED)

        def update_dot(dot, dt):
            x = self.x_axis.point_to_number(dot.get_center())
            slope = self.slope_of_tangent(x, graph)
            x -= slope*dt
            dot.move_to(self.input_to_graph_point(x, graph))

        self.add(*[
            Mobject.add_updater(dot, update_dot)
            for dot in dots
        ])
        self.wait(10)
