# ==============================================================================
# Scene:      ShowPlan
# Source:     videos/_2017/nn/part2.py (lines 91-125)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl ShowPlan.py ShowPlan -w -m --fps 15
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

class ShowPlan(Scene):
    def construct(self):
        title = OldTexText("Plan").scale(1.5)
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        h_line.set_color(WHITE)
        h_line.next_to(title, DOWN)
        self.add(title, h_line)

        items = VGroup(*[
            OldTexText("$\\cdot$ %s"%s)
            for s in [
                "Recap",
                "Gradient descent",
                "Analyze this network",
                "Where to learn more",
                "Research corner",
            ]
        ])
        items.arrange(DOWN, buff = MED_LARGE_BUFF, aligned_edge = LEFT)
        items.to_edge(LEFT, buff = LARGE_BUFF)

        rect = SurroundingRectangle(VGroup(*items[1:3]))

        self.add(items)
        self.wait()
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        for item in items[1:]:
            to_fade = VGroup(*[i for i in items if i is not item])
            self.play(
                to_fade.set_fill, None, 0.5,
                item.set_fill, None, 1,
            )
            self.wait()
