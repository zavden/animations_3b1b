# ==============================================================================
# Scene:      TwoGradientInterpretationsIn2D
# Source:     videos/_2017/nn/part2.py (lines 2431-2566)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl TwoGradientInterpretationsIn2D.py TwoGradientInterpretationsIn2D -w -m --fps 15
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

class TwoGradientInterpretationsIn2D(Scene):
    def construct(self):
        self.force_skipping()

        self.setup_plane()
        self.add_function_definitions()
        self.point_out_direction()
        self.point_out_relative_importance()
        self.wiggle_in_neighborhood()

    def setup_plane(self):
        plane = NumberPlane()
        plane.add_coordinates()
        self.add(plane)
        self.plane = plane

    def add_function_definitions(self):
        func = OldTex(
            "C(", "x, y", ")", "=", 
            "\\frac{3}{2}x^2", "+", "\\frac{1}{2}y^2",
        )
        func.shift(FRAME_X_RADIUS*LEFT/2).to_edge(UP)

        grad = OldTex("\\nabla", "C(", "1, 1", ")", "=")
        vect = OldTex(
            "\\left[\\begin{array}{c} 3 \\\\ 1 \\end{array}\\right]"
        )
        vect.next_to(grad, RIGHT, SMALL_BUFF)
        grad_group = VGroup(grad, vect)
        grad_group.next_to(ORIGIN, RIGHT).to_edge(UP, buff = MED_SMALL_BUFF)
        for mob in grad, vect, func:
            mob.add_background_rectangle()
            mob.background_rectangle.scale(1.1)

        self.play(Write(func, run_time = 1))
        self.play(Write(grad_group, run_time = 2))
        self.wait()

        self.func = func
        self.grad = grad
        self.vect = vect

    def point_out_direction(self):
        coords = self.grad.get_part_by_tex("1, 1").copy()
        vect = self.vect[1].copy()
        coords.set_color(YELLOW)
        vect.set_color(GREEN)

        dot = Dot(self.plane.coords_to_point(1, 1))
        dot.set_color(coords.get_color())
        arrow = Arrow(
            self.plane.coords_to_point(1, 1),
            self.plane.coords_to_point(4, 2),
            buff = 0,
            color = vect.get_color()
        )
        words = OldTexText("Direction of \\\\ steepest ascent")
        words.add_background_rectangle()
        words.next_to(ORIGIN, DOWN)
        words.rotate(arrow.get_angle())
        words.shift(arrow.get_center())

        self.play(DrawBorderThenFill(coords, run_time = 1))
        self.play(ReplacementTransform(coords.copy(), dot))
        self.play(DrawBorderThenFill(vect, run_time = 1))
        self.play(
            ReplacementTransform(vect.copy(), arrow),
            Animation(dot)
        )
        self.play(Write(words))
        self.wait()

        self.remove(vect)
        self.vect[1].set_color(vect.get_color())
        self.remove(coords)
        self.grad.get_part_by_tex("1, 1").set_color(coords.get_color())

        self.steepest_words = words
        self.dot = dot

    def point_out_relative_importance(self):
        func = self.func
        grad_group = VGroup(self.grad, self.vect)
        x_part = func.get_part_by_tex("x^2")
        y_part = func.get_part_by_tex("y^2")

        self.play(func.shift, 1.5*DOWN)

        x_rect = SurroundingRectangle(x_part, color = YELLOW)
        y_rect = SurroundingRectangle(y_part, color = TEAL)
        x_words = OldTexText("$x$ has 3 times \\\\ the impact...")
        x_words.set_color(x_rect.get_color())
        x_words.add_background_rectangle()
        x_words.next_to(x_rect, UP)
        # x_words.to_edge(LEFT)
        y_words = OldTexText("...as $y$")
        y_words.set_color(y_rect.get_color())
        y_words.add_background_rectangle()
        y_words.next_to(y_rect, DOWN)

        self.play(
            Write(x_words, run_time = 2),
            ShowCreation(x_rect)
        )
        self.wait()
        self.play(
            Write(y_words, run_time = 1),
            ShowCreation(y_rect)
        )
        self.wait(2)

    def wiggle_in_neighborhood(self):
        dot = self.dot
        steepest_words = self.steepest_words

        neighborhood = Circle(
            fill_color = BLUE,
            fill_opacity = 0.25,
            stroke_width = 0,
            radius = 0.5,
        )
        neighborhood.move_to(dot)

        self.revert_to_original_skipping_status()
        self.play(
            FadeOut(steepest_words),
            GrowFromCenter(neighborhood)
        )
        self.wait()
        for vect in RIGHT, UP, 0.3*(3*RIGHT + UP):
            self.play(
                dot.shift, 0.5*vect,
                rate_func = lambda t : wiggle(t, 4),
                run_time = 3,
            )
            self.wait()
