# ==============================================================================
# Scene:      MotivateSquishing
# Source:     videos/_2017/nn/part1.py (lines 2619-2715)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MotivateSquishing.py MotivateSquishing -w -m --fps 15
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


class MotivateSquishing(Scene):
    def construct(self):
        self.add_weighted_sum()
        self.show_real_number_line()
        self.show_interval()
        self.squish_into_interval()

    def add_weighted_sum(self):
        weighted_sum = OldTex(*it.chain(*[
            ["w_%d"%d, "a_%d"%d, "+"]
            for d in range(1, 5)
        ] + [
            ["\\cdots", "+", "w_n", "a_n"]
        ]))
        weighted_sum.set_color_by_tex("w_", GREEN)
        weighted_sum.to_edge(UP)
        self.add(weighted_sum)
        self.weighted_sum = weighted_sum

    def show_real_number_line(self):
        weighted_sum = self.weighted_sum
        number_line = NumberLine(unit_size = 1.5)
        number_line.add_numbers()
        number_line.shift(UP)
        arrow1, arrow2 = [
            Arrow(
                weighted_sum.get_bottom(),
                number_line.number_to_point(n),
            )
            for n in (-3, 3)
        ]

        self.play(Write(number_line))
        self.play(GrowFromPoint(arrow1, arrow1.get_start()))
        self.play(Transform(
            arrow1, arrow2,
            run_time = 5,
            rate_func = there_and_back
        ))
        self.play(FadeOut(arrow1))

        self.number_line = number_line

    def show_interval(self):
        lower_number_line = self.number_line.copy()
        lower_number_line.shift(2*DOWN)
        lower_number_line.set_color(GREY_B)
        lower_number_line.numbers.set_color(WHITE)
        interval = Line(
            lower_number_line.number_to_point(0),
            lower_number_line.number_to_point(1),
            color = YELLOW,
            stroke_width = 5
        )
        brace = Brace(interval, DOWN, buff = 0.7)
        words = OldTexText("Activations should be in this range")
        words.next_to(brace, DOWN, SMALL_BUFF)

        self.play(ReplacementTransform(
            self.number_line.copy(), lower_number_line
        ))
        self.play(
            GrowFromCenter(brace),
            GrowFromCenter(interval),
        )
        self.play(Write(words, run_time = 2))
        self.wait()

        self.lower_number_line = lower_number_line

    def squish_into_interval(self):
        line = self.number_line
        line.remove(*line.numbers)
        ghost_line = line.copy()
        ghost_line.fade(0.5)
        ghost_line.set_color(BLUE_E)
        self.add(ghost_line, line)
        lower_line = self.lower_number_line

        line.generate_target()
        u = line.unit_size
        line.target.apply_function(
            lambda p : np.array([u*sigmoid(p[0])]+list(p[1:]))
        )
        line.target.move_to(lower_line.number_to_point(0.5))

        arrow = Arrow(
            line.numbers.get_bottom(),
            line.target.get_top(),
            color = YELLOW
        )

        self.play(
            MoveToTarget(line),
            GrowFromPoint(arrow, arrow.get_start())
        )
        self.wait(2)
