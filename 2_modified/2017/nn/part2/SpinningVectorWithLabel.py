# ==============================================================================
# Scene:      SpinningVectorWithLabel
# Source:     videos/_2017/nn/part2.py (lines 2387-2429)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl SpinningVectorWithLabel.py SpinningVectorWithLabel -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Python 2 integer division used as an index/count -> //.
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

POSITIVE_COLOR = BLUE


NEGATIVE_COLOR = RED


def get_decimal_vector(nums, with_dots = True):
    decimals = VGroup()
    for num in nums:
        decimal = DecimalNumber(num)
        if num > 0:
            decimal.set_color(POSITIVE_COLOR)
        else:
            decimal.set_color(NEGATIVE_COLOR)
        decimals.add(decimal)
    contents = VGroup(*decimals)
    if with_dots:
        dots = OldTex("\\vdots")
        contents.submobjects.insert(len(decimals)//2, dots)  # CHANGE: Python 2 integer division used as an index/count -> //.
    contents.arrange(DOWN)
    lb, rb = brackets = OldTex("\\big[", "\\big]")
    brackets.scale(2)
    brackets.stretch_to_fit_height(1.2*contents.get_height())
    lb.next_to(contents, LEFT, SMALL_BUFF)
    rb.next_to(contents, RIGHT, SMALL_BUFF)

    result = VGroup(lb, contents, brackets)
    result.lb = lb
    result.rb = rb
    result.brackets = brackets
    result.decimals = decimals
    result.contents = contents
    if with_dots:
        result.dots = dots
    return result


class SpinningVectorWithLabel(Scene):
    def construct(self):
        plane = NumberPlane(
            x_unit_size = 2,
            y_unit_size = 2,
        )
        plane.add_coordinates()
        self.add(plane)

        vector = Vector(2*RIGHT)
        label = get_decimal_vector([-1, -1], with_dots = False)
        label.add_to_back(BackgroundRectangle(label))
        label.next_to(vector.get_end(), UP+RIGHT)
        label.decimals.set_fill(opacity = 0)
        decimals = label.decimals.copy()
        decimals.set_fill(WHITE, 1)

        cd1 = ChangingDecimal(
            decimals[0],
            lambda a : np.cos(vector.get_angle()),
            tracked_mobject = label.decimals[0],
        )
        cd2 = ChangingDecimal(
            decimals[1],
            lambda a : np.sin(vector.get_angle()),
            tracked_mobject = label.decimals[1],
        )

        self.play(
            Rotate(
                vector, 
                0.999*np.pi,
                in_place = False,
                run_time = 8,
                rate_func = there_and_back
            ),
            UpdateFromFunc(
                label,
                lambda m : m.next_to(vector.get_end(), UP+RIGHT)
            ),
            cd1, cd2,
        )
        self.wait()
