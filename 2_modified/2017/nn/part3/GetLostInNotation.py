# ==============================================================================
# Scene:      GetLostInNotation
# Source:     videos/_2017/nn/part3.py (lines 350-416)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl GetLostInNotation.py GetLostInNotation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

#### Libraries
# Standard library
import os
import random
import sys
import os.path
from manim_imports_ext import *
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



# ----- From _2017/nn/part3.py -----

class GetLostInNotation(PiCreatureScene):
    def construct(self):
        morty = self.pi_creature
        equations = VGroup(
            OldTex(
                "\\delta", "^L", "=", "\\nabla_a", "C", 
                "\\odot \\sigma'(", "z", "^L)"
            ),
            OldTex(
                "\\delta", "^l = ((", "w", "^{l+1})^T", 
                "\\delta", "^{l+1}) \\odot \\sigma'(", "z", "^l)"
            ),
            OldTex(
                "{\\partial", "C", "\\over \\partial", "b", 
                "_j^l} =", "\\delta", "_j^l"
            ),
            OldTex(
                "{\\partial", "C", " \\over \\partial", 
                "w", "_{jk}^l} = ", "a", "_k^{l-1}", "\\delta", "_j^l"
            ),
        )
        for equation in equations:
            equation.set_color_by_tex_to_color_map({
                "\\delta" : YELLOW,
                "C" : RED,
                "b" : MAROON_B,
                "w" : BLUE,
                "z" : TEAL,
            })
            equation.set_color_by_tex("nabla", WHITE)
        equations.arrange(
            DOWN, buff = MED_LARGE_BUFF, aligned_edge = LEFT
        )

        circle = Circle(radius = 3*FRAME_X_RADIUS)
        circle.set_fill(WHITE, 0)
        circle.set_stroke(WHITE, 0)

        self.play(
            Write(equations),
            morty.change, "confused", equations
        )
        self.wait()
        self.play(morty.change, "pleading")
        self.wait(2)

        ##
        movers = VGroup(*equations.family_members_with_points())
        random.shuffle(movers.submobjects)
        for mover in list(movers):
            if mover.is_subpath:
                movers.remove(mover)
                continue
            mover.set_stroke(WHITE, width = 0)
            mover.target = Circle()
            mover.target.scale(0.5)
            mover.target.set_fill(mover.get_color(), opacity = 0)
            mover.target.set_stroke(BLACK, width = 1)
            mover.target.move_to(mover)
        self.play(
            LaggedStartMap(
                MoveToTarget, movers,
                run_time = 2,
            ),
            morty.change, "pondering",
        )
        self.wait()
