# ==============================================================================
# Scene:      ExampleThrees
# Source:     videos/_2017/nn/part1.py (lines 336-525)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExampleThrees.py ExampleThrees -w -m --fps 15
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


class WrappedImage(Group):
    CONFIG = {
        "rect_kwargs" : {
            "color" : BLUE,
            "buff" : SMALL_BUFF,
        }
    }
    def __init__(self, image_mobject, **kwargs):
        Group.__init__(self, **kwargs)
        rect = SurroundingRectangle(
            image_mobject, **self.rect_kwargs
        )
        self.add(rect, image_mobject)


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


class ExampleThrees(PiCreatureScene):
    def construct(self):
        self.show_initial_three()
        self.show_alternate_threes()
        self.resolve_remaining_threes()
        self.show_alternate_digits()

    def show_initial_three(self):
        randy = self.pi_creature

        self.three_mobs = self.get_three_mobs()
        three_mob = self.three_mobs[0]
        three_mob_copy = three_mob[1].copy()
        three_mob_copy.sort(lambda p : np.dot(p, DOWN+RIGHT))

        braces = VGroup(*[Brace(three_mob, v) for v in (LEFT, UP)])
        brace_labels = VGroup(*[
            brace.get_text("28px")
            for brace in braces
        ])

        bubble = randy.get_bubble(height = 4, width = 6)
        three_mob.generate_target()
        three_mob.target.set_height(1)
        three_mob.target.next_to(bubble[-1].get_left(), RIGHT, LARGE_BUFF)
        arrow = Arrow(LEFT, RIGHT, color = BLUE)
        arrow.next_to(three_mob.target, RIGHT)
        real_three = OldTex("3")
        real_three.set_height(0.8)
        real_three.next_to(arrow, RIGHT)

        self.play(
            FadeIn(three_mob[0]),
            LaggedStartMap(FadeIn, three_mob[1])
        )
        self.wait()
        self.play(
            LaggedStartMap(
                DrawBorderThenFill, three_mob_copy,
                run_time = 3,
                stroke_color = WHITE,
                remover = True,
            ),
            randy.change, "sassy",
            *it.chain(
                list(map(GrowFromCenter, braces)),
                list(map(FadeIn, brace_labels))
            )
        )
        self.wait()
        self.play(
            ShowCreation(bubble),
            MoveToTarget(three_mob),
            FadeOut(braces),
            FadeOut(brace_labels),
            randy.change, "pondering"
        )
        self.play(
            ShowCreation(arrow),
            Write(real_three)
        )
        self.wait()

        self.bubble = bubble
        self.arrow = arrow
        self.real_three = real_three

    def show_alternate_threes(self):
        randy = self.pi_creature

        three = self.three_mobs[0]
        three.generate_target()
        three.target[0].set_fill(opacity = 0, family = False)
        for square in three.target[1]:
            yellow_rgb = color_to_rgb(YELLOW)
            square_rgb = color_to_rgb(square.get_fill_color())
            square.set_fill(
                rgba_to_color(yellow_rgb*square_rgb),
                opacity = 0.5
            )

        alt_threes = VGroup(*self.three_mobs[1:])
        alt_threes.arrange(DOWN)
        alt_threes.set_height(FRAME_HEIGHT - 2)
        alt_threes.to_edge(RIGHT)

        for alt_three in alt_threes:
            self.add(alt_three)
            self.wait(0.5)
        self.play(
            randy.change, "plain",
            *list(map(FadeOut, [
                self.bubble, self.arrow, self.real_three
            ])) + [MoveToTarget(three)]
        )
        for alt_three in alt_threes[:2]:
            self.play(three.replace, alt_three)
            self.wait()
        for moving_three in three, alt_threes[1]:
            moving_three.generate_target()
            moving_three.target.next_to(alt_threes, LEFT, LARGE_BUFF)
            moving_three.target[0].set_stroke(width = 0)
            moving_three.target[1].space_out_submobjects(1.5)
            self.play(MoveToTarget(
                moving_three, lag_ratio = 0.5
            ))
            self.play(
                Animation(randy),
                moving_three.replace, randy.eyes[1],
                moving_three.scale, 0.7,
                run_time = 2,
                lag_ratio = 0.5,
            )
            self.play(
                Animation(randy),
                FadeOut(moving_three)
            )

        self.remaining_threes = [alt_threes[0], alt_threes[2]]

    def resolve_remaining_threes(self):
        randy = self.pi_creature

        left_three, right_three = self.remaining_threes
        equals = OldTex("=")
        equals.move_to(self.arrow)
        for three, vect in (left_three, LEFT), (right_three, RIGHT):
            three.generate_target()
            three.target.set_height(1)
            three.target.next_to(equals, vect)

        self.play(
            randy.change, "thinking",
            ShowCreation(self.bubble),
            MoveToTarget(left_three),
            MoveToTarget(right_three),
            Write(equals),
        )
        self.wait()

        self.equals = equals

    def show_alternate_digits(self):
        randy = self.pi_creature
        cross = Cross(self.equals)
        cross.stretch_to_fit_height(0.5)
        three = self.remaining_threes[1]

        image_map = get_organized_images()
        arrays = [image_map[k][0] for k in range(8, 4, -1)]
        alt_mobs = [
            WrappedImage(
                PixelsAsSquares(ImageMobject(layer_to_image_array(arr))),
                color = GREY_B,
                buff = 0
            ).replace(three)
            for arr in arrays
        ]

        self.play(
            randy.change, "sassy",
            Transform(three, alt_mobs[0]),
            ShowCreation(cross)
        )
        self.wait()
        for mob in alt_mobs[1:]:
            self.play(Transform(three, mob))
            self.wait()

    ######

    def create_pi_creature(self):
        return Randolph().to_corner(DOWN+LEFT)

    def get_three_mobs(self):
        three_arrays = get_organized_images()[3][:4]
        three_mobs = VGroup()
        for three_array in three_arrays:
            im_mob = ImageMobject(
                layer_to_image_array(three_array),
                height = 4,
            )
            pixel_mob = PixelsAsSquares(im_mob)
            three_mob = WrappedImage(
                pixel_mob,
                color = GREY_B,
                buff = 0
            )
            three_mobs.add(three_mob)
        return three_mobs
