# ==============================================================================
# Scene:      BrainAndHow
# Source:     videos/_2017/nn/part1.py (lines 527-550)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BrainAndHow.py BrainAndHow -w -m --fps 15
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


class BrainAndHow(Scene):
    def construct(self):
        brain = SVGMobject(file_name = "brain")
        brain.set_height(2)
        brain.set_fill(GREY_B)
        brain_outline = brain.copy()
        brain_outline.set_fill(opacity = 0)
        brain_outline.set_stroke(BLUE_B, 3)

        how = OldTexText("How?!?")
        how.scale(2)
        how.next_to(brain, UP)

        self.add(brain)
        self.play(Write(how))
        for x in range(2):
            self.play(
                ShowPassingFlash(
                    brain_outline, 
                    time_width = 0.5,
                    run_time = 2
                )
            )
        self.wait()
