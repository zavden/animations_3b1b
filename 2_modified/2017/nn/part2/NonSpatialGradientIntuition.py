# ==============================================================================
# Scene:      NonSpatialGradientIntuition
# Source:     videos/_2017/nn/part2.py (lines 2157-2316)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl NonSpatialGradientIntuition.py NonSpatialGradientIntuition -w -m --fps 15
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

class NonSpatialGradientIntuition(Scene):
    CONFIG = {
        "w_color" : YELLOW,
        "positive_color" : BLUE,
        "negative_color" : RED,
        "vect_height" : FRAME_Y_RADIUS - MED_LARGE_BUFF,
        "text_scale_value" : 0.7,
    }
    def construct(self):
        self.add_vector()
        self.add_gradient()
        self.show_sign_interpretation()
        self.show_magnitude_interpretation()

    def add_vector(self):
        lhs = OldTex("\\vec{\\textbf{W}}", "=")
        lhs[0].set_color(self.w_color)
        lhs.to_edge(LEFT)

        ws = VGroup(*[
            VGroup(OldTex(tex))
            for tex in it.chain(
                ["w_%d"%d for d in range(3)],
                ["\\vdots"],
                ["w_{13{,}00%d}"%d for d in range(3)]
            )
        ])
        ws.set_color(self.w_color)
        ws.arrange(DOWN)
        lb, rb = brackets = OldTex("\\big[", "\\big]").scale(2)
        brackets.stretch_to_fit_height(1.2*ws.get_height())
        lb.next_to(ws, LEFT)
        rb.next_to(ws, RIGHT)
        vect = VGroup(lb, ws, rb)

        vect.set_height(self.vect_height)
        vect.to_edge(UP).shift(2*LEFT)
        lhs.next_to(vect, LEFT)

        self.add(lhs, vect)
        self.vect = vect
        self.top_lhs = lhs

    def add_gradient(self):
        lb, ws, rb = vect = self.vect
        ws = VGroup(*ws)
        # CHANGE: Python 2 integer division used as an index/count -> //.
        dots = ws[len(ws)//2]
        ws.remove(dots)

        lhs = OldTex(
            "-\\nabla", "C(", "\\vec{\\textbf{W}}", ")", "="
        )
        lhs.next_to(vect, RIGHT, LARGE_BUFF)
        lhs.set_color_by_tex("W", self.w_color)

        decimals = VGroup()
        nums = [0.31, 0.03, -1.25, 0.78, -0.37, 0.16]
        for num, w in zip(nums, ws):
            decimal = DecimalNumber(num)
            decimal.scale(self.text_scale_value)
            if num > 0:
                decimal.set_color(self.positive_color)
            else:
                decimal.set_color(self.negative_color)
            decimal.move_to(w)
            decimals.add(decimal)
        new_dots = dots.copy()

        grad_content = VGroup(*it.chain(
            decimals[:3], new_dots, decimals[3:]
        ))
        grad_vect = VGroup(lb.copy(), grad_content, rb.copy())
        VGroup(grad_vect[0], grad_vect[-1]).space_out_submobjects(0.8)
        grad_vect.set_height(self.vect_height)
        grad_vect.next_to(self.vect, DOWN)
        lhs.next_to(grad_vect, LEFT)

        brace = Brace(grad_vect, RIGHT)
        words = brace.get_text("Example gradient")

        self.wait()
        self.play(
            ReplacementTransform(self.top_lhs.copy(), lhs),
            ReplacementTransform(self.vect.copy(), grad_vect),
            GrowFromCenter(brace),
            FadeIn(words)
        )
        self.wait()
        self.play(FadeOut(VGroup(brace, words)))

        self.ws = ws
        self.grad_lhs = lhs
        self.grad_vect = grad_vect
        self.decimals = decimals

    def show_sign_interpretation(self):
        ws = self.ws.copy()
        decimals = self.decimals

        direction_phrases = VGroup()
        for w, decimal in zip(ws, decimals):
            if decimal.number > 0:
                verb = "increase"
                color = self.positive_color
            else:
                verb = "decrease"
                color = self.negative_color
            phrase = OldTexText("should", verb)
            phrase.scale(self.text_scale_value)
            phrase.set_color_by_tex(verb, color)
            w.generate_target()
            group = VGroup(w.target, phrase)
            group.arrange(RIGHT)
            w.target.shift(0.7*SMALL_BUFF*DOWN)
            group.move_to(decimal.get_center() + RIGHT, LEFT)
            direction_phrases.add(phrase)

        self.play(
            LaggedStartMap(MoveToTarget, ws),
            LaggedStartMap(FadeIn, direction_phrases)
        )
        self.wait(2)

        self.direction_phrases = direction_phrases
        self.ws = ws

    def show_magnitude_interpretation(self):
        direction_phrases = self.direction_phrases
        ws = self.ws
        decimals = self.decimals

        magnitude_words = VGroup()
        rects = VGroup()
        for phrase, decimal in zip(direction_phrases, decimals):
            if abs(decimal.number) < 0.2:
                adj = "a little"
                color = interpolate_color(BLACK, WHITE, 0.5)
            elif abs(decimal.number) < 0.5:
                adj = "somewhat"
                color = GREY_B
            else:
                adj = "a lot"
                color =  WHITE
            words = OldTexText(adj)
            words.scale(self.text_scale_value)
            words.set_color(color)
            words.next_to(phrase, RIGHT, SMALL_BUFF)
            magnitude_words.add(words)

            rect = SurroundingRectangle(
                VGroup(*decimal[-4:]), 
                buff = SMALL_BUFF,
                color = GREY_B
            )
            rect.target = words
            rects.add(rect)

        self.play(LaggedStartMap(ShowCreation, rects))
        self.play(LaggedStartMap(MoveToTarget, rects))
        self.wait(2)
