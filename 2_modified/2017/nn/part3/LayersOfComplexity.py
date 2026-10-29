# ==============================================================================
# Scene:      LayersOfComplexity
# Source:     videos/_2017/nn/part3.py (lines 4223-4285)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl LayersOfComplexity.py LayersOfComplexity -w -m --fps 15
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

class LayersOfComplexity(Scene):
    def construct(self):
        chain_rule_equations = self.get_chain_rule_equations()
        chain_rule_equations.to_corner(UP+RIGHT)

        brace = Brace(chain_rule_equations, LEFT)
        arrow = Vector(LEFT, color = RED)
        arrow.next_to(brace, LEFT)
        gradient = OldTex("\\nabla C")
        gradient.scale(2)
        gradient.set_color(RED)
        gradient.next_to(arrow, LEFT)

        self.play(LaggedStartMap(FadeIn, chain_rule_equations))
        self.play(GrowFromCenter(brace))
        self.play(GrowArrow(arrow))
        self.play(Write(gradient))
        self.wait()


    def get_chain_rule_equations(self):
        w_deriv = OldTex(
            "{\\partial C", "\\over", "\\partial w^{(l)}_{jk}}",
            "=",
            "a^{(l-1)}_k",
            "\\sigma'(z^{(l)}_j)",
            "{\\partial C", "\\over", "\\partial a^{(l)}_j}",
        )
        lil_rect = SurroundingRectangle(
            VGroup(*w_deriv[-3:]),
            buff = 0.5*SMALL_BUFF
        )
        a_deriv = OldTex(
            "\\sum_{j = 0}^{n_{l+1} - 1}",
            "w^{(l+1)}_{jk}",
            "\\sigma'(z^{(l+1)}_j)",
            "{\\partial C", "\\over", "\\partial a^{(l+1)}_j}",
        )
        or_word = OldTexText("or")
        last_a_deriv = OldTex("2(a^{(L)}_j - y_j)")

        a_deriv.next_to(w_deriv, DOWN, LARGE_BUFF)
        or_word.next_to(a_deriv, DOWN)
        last_a_deriv.next_to(or_word, DOWN, MED_LARGE_BUFF)

        big_rect = SurroundingRectangle(VGroup(a_deriv, last_a_deriv))
        arrow = Arrow(
            lil_rect.get_corner(DOWN+LEFT), 
            big_rect.get_top(),
        )

        result = VGroup(
            w_deriv, lil_rect, arrow,
            big_rect, a_deriv, or_word, last_a_deriv
        )
        for expression in w_deriv, a_deriv, last_a_deriv:
            expression.set_color_by_tex_to_color_map({
                "C" : RED,
                "z^" : GREEN,
                "w^" : BLUE,
                "b^" : MAROON_B,
            })
        return result
