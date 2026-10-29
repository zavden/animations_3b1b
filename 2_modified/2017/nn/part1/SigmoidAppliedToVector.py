# ==============================================================================
# Scene:      SigmoidAppliedToVector
# Source:     videos/_2017/nn/part1.py (lines 3903-3926)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SigmoidAppliedToVector.py SigmoidAppliedToVector -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - OldTex piece indices differ (29 glyphs instead of 37 pieces): highlight every glyph except the variables and '='.
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


class SigmoidAppliedToVector(Scene):
    def construct(self):
        tex = OldTex("""
            \\sigma \\left(
            \\left[\\begin{array}{c}
                x \\\\ y \\\\ z
            \\end{array}\\right]
            \\right) =
            \\left[\\begin{array}{c}
                \\sigma(x) \\\\ \\sigma(y) \\\\ \\sigma(z)
            \\end{array}\\right]
        """)
        tex.set_width(FRAME_WIDTH - 1)
        tex.to_edge(DOWN)
        # CHANGE: OldTex piece indices differ (29 glyphs instead of 37 pieces): highlight every glyph except the variables and '='.
        # Cairo split the TeX into 37 pieces, GL gives 29 glyphs: highlight every sigma and every bracket / parenthesis
        # (all glyphs except the variables x, y, z and the equals sign).
        indices = [i for i in range(len(tex)) if i not in (5, 6, 7, 12, 17, 21, 25)]
        for i in indices:
            tex[i].set_color(YELLOW)
        self.add(tex)
        self.wait()
