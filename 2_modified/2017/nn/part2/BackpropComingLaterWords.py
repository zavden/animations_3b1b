# ==============================================================================
# Scene:      BackpropComingLaterWords
# Source:     videos/_2017/nn/part2.py (lines 323-328)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl BackpropComingLaterWords.py BackpropComingLaterWords -w -m --fps 15
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

class BackpropComingLaterWords(Scene):
    def construct(self):
        words = OldTexText("(Backpropagation be \\\\ the next video)")
        words.set_width(FRAME_WIDTH-1)
        words.to_edge(DOWN)
        self.add(words)
