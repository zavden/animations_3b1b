# ==============================================================================
# Scene:      NotPerfectAddOn
# Source:     videos/_2017/nn/part1.py (lines 904-918)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NotPerfectAddOn.py NotPerfectAddOn -w -m --fps 15
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


class NotPerfectAddOn(Scene):
    def construct(self):
        words = OldTexText("Not perfect!")
        words.scale(1.5)
        arrow = Arrow(UP+RIGHT, DOWN+LEFT, color = RED)
        words.set_color(RED)
        arrow.to_corner(DOWN+LEFT)
        words.next_to(arrow, UP+RIGHT)

        self.play(
            Write(words),
            ShowCreation(arrow),
            run_time = 1
        )
        self.wait(2)
