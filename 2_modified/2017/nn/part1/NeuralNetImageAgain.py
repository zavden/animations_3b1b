# ==============================================================================
# Scene:      NeuralNetImageAgain
# Source:     videos/_2017/nn/part1.py (lines 4617-4663)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NeuralNetImageAgain.py NeuralNetImageAgain -w -m --fps 15
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


class NeuralNetImageAgain(Scene):
    def construct(self):
        layers = VGroup()
        for length in [16, 16, 16, 10]:
            circs = VGroup(*[
                Circle(radius=1)
                for x in range(length)
            ])
            circs.arrange(DOWN, buff=0.5)
            circs.set_stroke(WHITE, 2)
            layers.add(circs)
        layers.set_height(6.5)
        layers.arrange(RIGHT, buff=2.5)

        dots = OldTex("\\vdots")
        dots.move_to(layers[0])
        layers[0][:8].next_to(dots, UP, MED_SMALL_BUFF)
        layers[0][8:].next_to(dots, DOWN, MED_SMALL_BUFF)

        for layer in layers[1:3]:
            for node in layer:
                node.set_fill(WHITE, opacity=random.random())
        layers[3][6].set_fill(WHITE, 0.9)

        all_edges = VGroup()
        for l1, l2 in zip(layers, layers[1:]):
            edges = VGroup()
            for n1, n2 in it.product(l1, l2):
                edge = Line(
                    n1.get_center(), n2.get_center(),
                    buff=n1.get_height() / 2
                )
                edge.set_stroke(WHITE, 1, opacity=0.75)
                # edge.set_stroke(
                #     color=random.choice([BLUE, RED]),
                #     width=3 * random.random()**6,
                #     # opacity=0.5
                # )
                edges.add(edge)
            all_edges.add(edges)

        network = VGroup(all_edges, layers, dots)

        brace = Brace(network, LEFT)

        self.add(network)
        self.add(brace)
