# ==============================================================================
# Scene:      WriteAProgram
# Source:     videos/_2017/nn/part1.py (lines 552-617)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WriteAProgram.py WriteAProgram -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - `Tex(` here is the NEW GL class (different piece splitting, 'Tex' vs 'OldTex'); the Cairo code meant TexMobject -> OldTex.
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


class PixelsAsSquares(VGroup):
    CONFIG = {
        "height" : 2,
    }
    def __init__(self, image_mobject, **kwargs):
        VGroup.__init__(self, **kwargs)
        for row in image_mobject.pixel_array:
            for rgba in row:
                square = Square(
                    stroke_width = 0, 
                    fill_opacity = rgba[3]/255.0,
                    fill_color = rgba_to_color(rgba/255.0),
                )
                self.add(square)
        self.arrange_in_grid(
            *image_mobject.pixel_array.shape[:2],
            buff = 0
        )
        self.replace(image_mobject)


class WriteAProgram(Scene):
    def construct(self):
        three_array = get_organized_images()[3][0]
        im_mob = ImageMobject(layer_to_image_array(three_array))
        three = PixelsAsSquares(im_mob)
        three.sort(lambda p : np.dot(p, DOWN+RIGHT))
        three.set_height(6)
        three.next_to(ORIGIN, LEFT)
        three_rect = SurroundingRectangle(
            three, 
            color = BLUE,
            buff = SMALL_BUFF
        )

        numbers = VGroup()
        for square in three:
            rgb = square.fill_rgb
            num = DecimalNumber(
                square.fill_rgb[0],
                num_decimal_places = 1
            )
            num.set_stroke(width = 1)
            color = rgba_to_color(1 - (rgb + 0.2)/1.2)
            num.set_color(color)
            num.set_width(0.7*square.get_width())
            num.move_to(square)
            numbers.add(num)

        arrow = Arrow(LEFT, RIGHT, color = BLUE)
        arrow.next_to(three, RIGHT)

        choices = VGroup(*[OldTex(str(n)) for n in range(10)])  # CHANGE: `Tex(` here is the NEW GL class (different piece splitting, ...
        choices.arrange(DOWN)
        choices.set_height(FRAME_HEIGHT - 1)
        choices.next_to(arrow, RIGHT)

        self.play(
            LaggedStartMap(DrawBorderThenFill, three),
            ShowCreation(three_rect)
        )
        self.play(Write(numbers))
        self.play(
            ShowCreation(arrow),
            LaggedStartMap(FadeIn, choices),
        )

        rect = SurroundingRectangle(choices[0], buff = SMALL_BUFF)
        q_mark = OldTex("?")
        q_mark.next_to(rect, RIGHT)
        self.play(ShowCreation(rect))
        for n in 8, 1, 5, 3:
            self.play(
                rect.move_to, choices[n],
                MaintainPositionRelativeTo(q_mark, rect)
            )
            self.wait(1)
        choice = choices[3]
        choices.remove(choice)
        choice.add(rect)
        self.play(
            choice.scale, 1.5, 
            choice.next_to, arrow, RIGHT,
            FadeOut(choices),
            FadeOut(q_mark),
        )
        self.wait(2)
