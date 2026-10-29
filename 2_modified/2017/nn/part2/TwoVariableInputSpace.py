# ==============================================================================
# Scene:      TwoVariableInputSpace
# Source:     videos/_2017/nn/part2.py (lines 1819-1924)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl TwoVariableInputSpace.py TwoVariableInputSpace -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - `map(Tex, ...)` used the NEW GL Tex class; the Cairo code meant TexMobject -> OldTex.
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

class TwoVariableInputSpace(Scene):
    def construct(self):
        self.add_plane()
        self.ask_about_direction()
        self.show_gradient()

    def add_plane(self):
        plane = NumberPlane(
            x_radius = FRAME_X_RADIUS/2
        )
        plane.add_coordinates()
        name = OldTexText("Input space")
        name.add_background_rectangle()
        name.next_to(plane.get_corner(UP+LEFT), DOWN+RIGHT)
        x, y = list(map(OldTex, ["x", "y"]))  # CHANGE: map(Tex) -> map(OldTex) (Cairo TexMobject)
        x.next_to(plane.coords_to_point(3.25, 0), UP, SMALL_BUFF)
        y.next_to(plane.coords_to_point(0, 3.6), RIGHT, SMALL_BUFF)

        self.play(
            *list(map(Write, [plane, name, x, y])),
            run_time = 1
        )
        self.wait()

        self.plane = plane

    def ask_about_direction(self):
        point = self.plane.coords_to_point(2, 1)
        dot = Dot(point, color = YELLOW)
        dot.save_state()
        dot.move_to(FRAME_Y_RADIUS*UP + FRAME_X_RADIUS*RIGHT/2)
        dot.fade(1)
        arrows = VGroup(*[
            Arrow(ORIGIN, vect).shift(point)
            for vect in compass_directions(8)
        ])
        arrows.set_color(WHITE)
        question = OldTexText(
            "Which direction decreases \\\\",
            "$C(x, y)$", "most quickly?"
        )
        question.scale(0.7)
        question.set_color(YELLOW)
        question.set_color_by_tex("C(x, y)", RED)
        question.add_background_rectangle()
        question.next_to(arrows, LEFT)

        self.play(dot.restore)
        self.play(
            FadeIn(question),
            LaggedStartMap(GrowArrow, arrows)
        )
        self.wait()

        self.arrows = arrows
        self.dot = dot
        self.question = question

    def show_gradient(self):
        arrows = self.arrows
        dot = self.dot
        question = self.question

        arrow = arrows[3]
        new_arrow = Arrow(
            dot.get_center(), arrow.get_end(),
            buff = 0,
            color = GREEN
        )
        new_arrow.set_color(GREEN)
        arrow.save_state()

        gradient = OldTex("\\nabla C(x, y)")
        gradient.add_background_rectangle()
        gradient.next_to(arrow.get_end(), UP, SMALL_BUFF)

        gradient_words = OldTexText(
            "``Gradient'', the direction\\\\ of",
            "steepest increase"
        )
        gradient_words.scale(0.7)
        gradient_words[-1].set_color(GREEN)
        gradient_words.next_to(gradient, UP, SMALL_BUFF)
        gradient_words.add_background_rectangle(opacity = 1)
        gradient_words.shift(LEFT)

        anti_arrow = new_arrow.copy()
        anti_arrow.rotate(np.pi, about_point = dot.get_center())
        anti_arrow.set_color(RED)

        self.play(
            Transform(arrow, new_arrow),
            Animation(dot),
            *[FadeOut(a) for a in arrows if a is not arrow]
        )
        self.play(FadeIn(gradient))
        self.play(Write(gradient_words, run_time = 2))
        self.wait(2)
        self.play(
            arrow.fade,
            ReplacementTransform(
                arrow.copy(),
                anti_arrow
            )
        )
        self.wait(2)
