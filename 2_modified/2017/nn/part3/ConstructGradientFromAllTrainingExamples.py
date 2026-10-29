# ==============================================================================
# Scene:      ConstructGradientFromAllTrainingExamples
# Source:     videos/_2017/nn/part3.py (lines 1463-1831)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py
#
# Run from this folder:
#     manimgl ConstructGradientFromAllTrainingExamples.py ConstructGradientFromAllTrainingExamples -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Inlined network.py: data files (image_map, pretrained weights) live in the bundled nn/ folder next to the scene.
#   - Pickle data files must be opened in binary mode in Python 3.
#   - `map(Tex, ...)` used the NEW GL Tex class; the Cairo code meant TexMobject -> OldTex.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
# ==============================================================================

#### Libraries
# Standard library
import os
import pickle
import random
# Third-party libraries
import numpy as np
# CHANGE: Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
import sys, os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # CL17-B
from nn.mnist_loader import load_data_wrapper
import sys
import os.path
from manim_imports_ext import *
import warnings
from nn.network import *


# ----- From _2017/nn/network.py -----

# CHANGE: Inlined network.py: data files (image_map, pretrained weights) live in the bundled nn/ folder next to the scene.
NN_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nn")  # CL17-B nndir
IMAGE_MAP_DATA_FILE = os.path.join(NN_DIRECTORY, "image_map")


def layer_to_image_array(layer):
    w = int(np.ceil(np.sqrt(len(layer))))
    if len(layer) < w**2:
        layer = np.append(layer, np.zeros(w**2 - len(layer)))
    layer = layer.reshape((w, w))
    # return Image.fromarray((255*layer).astype('uint8'))
    return (255*layer).astype('int')


def get_organized_images():
    # CHANGE: Pickle data files must be opened in binary mode in Python 3.
    data_file = open(IMAGE_MAP_DATA_FILE, mode = 'rb')
    image_map = pickle.load(data_file, encoding='latin1')
    data_file.close()
    return image_map



# ----- From _2017/nn/part1.py -----

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


class MNistMobject(WrappedImage):
    def __init__(self, vect, **kwargs):
        WrappedImage.__init__(self, 
            ImageMobject(layer_to_image_array(vect)),
            **kwargs
        )



# ----- From _2017/nn/part3.py -----

class ConstructGradientFromAllTrainingExamples(Scene):
    CONFIG = { 
        "image_height" : 0.9,
        "eyes_height" : 0.25,
        "n_examples" : 6,
        "change_scale_val" : 0.8,
    }
    def construct(self):
        self.setup_grid()
        self.setup_weights()
        self.show_two_requesting_changes()
        self.show_all_examples_requesting_changes()
        self.average_together()
        self.collapse_into_gradient_vector()

    def setup_grid(self):
        h_lines = VGroup(*[
            Line(LEFT, RIGHT).scale(0.85*FRAME_X_RADIUS)
            for x in range(6)
        ])
        h_lines.arrange(DOWN, buff = 1)
        h_lines.set_stroke(GREY_B, 2)
        h_lines.to_edge(DOWN, buff = MED_LARGE_BUFF)
        h_lines.to_edge(LEFT, buff = 0)

        v_lines = VGroup(*[
            Line(UP, DOWN).scale(FRAME_Y_RADIUS - MED_LARGE_BUFF)
            for x in range(self.n_examples + 1)
        ])
        v_lines.arrange(RIGHT, buff = 1.4)
        v_lines.set_stroke(GREY_B, 2)
        v_lines.to_edge(LEFT, buff = 2)

        # self.add(h_lines, v_lines)
        self.h_lines = h_lines
        self.v_lines = v_lines

    def setup_weights(self):
        weights = VGroup(*list(map(OldTex, [  # CHANGE: map(Tex) -> map(OldTex) (Cairo TexMobject)
            "w_0", "w_1", "w_2", "\\vdots", "w_{13{,}001}"
        ])))
        for i, weight in enumerate(weights):
            weight.move_to(self.get_grid_position(i, 0))
        weights.to_edge(LEFT, buff = MED_SMALL_BUFF)

        brace = Brace(weights, RIGHT)
        weights_words = brace.get_text("All weights and biases")

        self.add(weights, brace, weights_words)
        self.set_variables_as_attrs(
            weights, brace, weights_words,
            dots = weights[-2]
        )

    def show_two_requesting_changes(self):
        two = self.get_example(get_organized_images()[2][0], 0)
        self.two = two
        self.add(two)

        self.two_changes = VGroup()
        for i in list(range(3)) + [4]:
            weight = self.weights[i]
            bubble, change = self.get_requested_change_bubble(two)
            weight.save_state()
            weight.generate_target()
            weight.target.next_to(two, RIGHT, aligned_edge = DOWN)

            self.play(
                MoveToTarget(weight),
                two.eyes.look_at_anim(weight.target),
                FadeIn(bubble),
                Write(change, run_time = 1),
            )
            if random.random() < 0.5:
                self.play(two.eyes.blink_anim())
            else:
                self.wait()
            if i == 0:
                added_anims = [
                    FadeOut(self.brace),
                    FadeOut(self.weights_words),
                ]
            elif i == 4:
                dots_copy = self.dots.copy()
                added_anims = [
                    dots_copy.move_to,
                    self.get_grid_position(3, 0)
                ]
                self.first_column_dots = dots_copy
            else:
                added_anims = []
            self.play(
                FadeOut(bubble),
                weight.restore,
                two.eyes.look_at_anim(weight.saved_state),
                change.restore,
                change.scale, self.change_scale_val,
                change.move_to, self.get_grid_position(i, 0),
                *added_anims
            )
            self.two_changes.add(change)
        self.wait()

    def show_all_examples_requesting_changes(self):
        training_data, validation_data, test_data = load_data_wrapper()
        data = training_data[:self.n_examples-1]
        examples = VGroup(*[
            self.get_example(t[0], j)
            for t, j in zip(data, it.count(1))
        ])
        h_dots = OldTex("\\dots")
        h_dots.next_to(examples, RIGHT, MED_LARGE_BUFF)
        more_h_dots = VGroup(*[
            OldTex("\\dots").move_to(
                self.get_grid_position(i, self.n_examples)
            )
            for i in range(5)
        ])
        more_h_dots.shift(MED_LARGE_BUFF*RIGHT)
        more_h_dots[-2].rotate(-np.pi/4)
        more_v_dots = VGroup(*[
            self.dots.copy().move_to(
                self.get_grid_position(3, j)
            )
            for j in range(1, self.n_examples)
        ])

        changes = VGroup(*[
            self.get_random_decimal().move_to(
                self.get_grid_position(i, j)
            )
            for i in list(range(3)) + [4]
            for j in range(1, self.n_examples)
        ])
        for change in changes:
            change.scale(self.change_scale_val)

        self.play(
            LaggedStartMap(FadeIn, examples),
            LaggedStartMap(ShowCreation, self.h_lines),
            LaggedStartMap(ShowCreation, self.v_lines),
            Write(
                h_dots, 
                run_time = 2, 
                rate_func = squish_rate_func(smooth, 0.7, 1)
            )
        )
        self.play(
            Write(changes),
            Write(more_v_dots),
            Write(more_h_dots),
            *[
                example.eyes.look_at_anim(random.choice(changes))
                for example in examples
            ]
        )
        for x in range(2):
            self.play(random.choice(examples).eyes.blink_anim())

        k = self.n_examples - 1
        self.change_rows = VGroup(*[
            VGroup(two_change, *changes[k*i:k*(i+1)])
            for i, two_change in enumerate(self.two_changes)
        ])
        for i in list(range(3)) + [-1]:
            self.change_rows[i].add(more_h_dots[i])

        self.all_eyes = VGroup(*[
            m.eyes for m in [self.two] + list(examples)
        ])

        self.set_variables_as_attrs(
            more_h_dots, more_v_dots,
            h_dots, changes,
        )

    def average_together(self):
        rects = VGroup()
        arrows = VGroup()
        averages = VGroup()
        for row in self.change_rows:
            rect = SurroundingRectangle(row)
            arrow = Arrow(ORIGIN, RIGHT)
            arrow.next_to(rect, RIGHT)
            rect.arrow = arrow
            average = self.get_colored_decimal(3*np.mean([
                m.number for m in row 
                if isinstance(m, DecimalNumber)
            ]))
            average.scale(self.change_scale_val)
            average.next_to(arrow, RIGHT)
            row.target = VGroup(average)

            rects.add(rect)
            arrows.add(arrow)
            averages.add(average)

        words = OldTexText("Average over \\\\ all training data")
        words.scale(0.8)
        words.to_corner(UP+RIGHT)
        arrow_to_averages = Arrow(
            words.get_bottom(), averages.get_top(),
            color = WHITE
        )

        dots = self.dots.copy()
        dots.move_to(VGroup(*averages[-2:]))

        look_at_anims = self.get_look_at_anims

        self.play(Write(words, run_time = 1), *look_at_anims(words))
        self.play(ShowCreation(rects[0]), *look_at_anims(rects[0]))
        self.play(
            ReplacementTransform(rects[0].copy(), arrows[0]),
            rects[0].set_stroke, WHITE, 1,
            ReplacementTransform(
                self.change_rows[0].copy(),
                self.change_rows[0].target
            ),
            *look_at_anims(averages[0])
        )
        self.play(GrowArrow(arrow_to_averages))
        self.play(
            LaggedStartMap(ShowCreation, VGroup(*rects[1:])),
            *look_at_anims(rects[1])
        )
        self.play(
            LaggedStartMap(
                ReplacementTransform, VGroup(*rects[1:]).copy(),
                lambda m : (m, m.arrow),
                lag_ratio = 0.7,
            ),
            VGroup(*rects[1:]).set_stroke, WHITE, 1,
            LaggedStartMap(
                ReplacementTransform, VGroup(*self.change_rows[1:]).copy(),
                lambda m : (m, m.target),
                lag_ratio = 0.7,
            ),
            Write(dots),
            *look_at_anims(averages[1])
        )
        self.blink(3)
        self.wait()

        averages.add(dots)
        self.set_variables_as_attrs(
            rects, arrows, averages,
            arrow_to_averages
        )

    def collapse_into_gradient_vector(self):
        averages = self.averages
        lb, rb = brackets = OldTex("[]")
        brackets.scale(2)
        brackets.stretch_to_fit_height(1.2*averages.get_height())
        lb.next_to(averages, LEFT, SMALL_BUFF)
        rb.next_to(averages, RIGHT, SMALL_BUFF)
        brackets.set_fill(opacity = 0)

        shift_vect = 2*LEFT

        lhs = OldTex(
            "-", "\\nabla", "C(",
            "w_1,", "w_2,", "\\dots", "w_{13{,}001}",
            ")", "="
        )
        lhs.next_to(lb, LEFT)
        lhs.shift(shift_vect)
        minus = lhs[0]
        w_terms = lhs.get_parts_by_tex("w_")
        dots_term = lhs.get_part_by_tex("dots")
        eta = OldTex("\\eta")
        eta.move_to(minus, RIGHT)
        eta.set_color(MAROON_B)

        to_fade = VGroup(*it.chain(
            self.h_lines, self.v_lines,
            self.more_h_dots, self.more_v_dots,
            self.change_rows, 
            self.first_column_dots,
            self.rects,
            self.arrows,
        ))
        arrow = self.arrow_to_averages

        self.play(LaggedStartMap(FadeOut, to_fade))
        self.play(
            brackets.shift, shift_vect,
            brackets.set_fill, WHITE, 1,
            averages.shift, shift_vect,
            Transform(arrow, Arrow(
                arrow.get_start(),
                arrow.get_end() + shift_vect,
                buff = 0,
                color = arrow.get_color(),
            )),
            FadeIn(VGroup(*lhs[:3])),
            FadeIn(VGroup(*lhs[-2:])),
            *self.get_look_at_anims(lhs)
        )
        self.play(
            ReplacementTransform(self.weights, w_terms),
            ReplacementTransform(self.dots, dots_term),
            *self.get_look_at_anims(w_terms)
        )
        self.blink(2)
        self.play(
            GrowFromCenter(eta),
            minus.shift, MED_SMALL_BUFF*LEFT
        )
        self.wait()

    ####

    def get_example(self, in_vect, index):
        result = MNistMobject(in_vect)
        result.set_height(self.image_height)

        eyes = Eyes(result, height = self.eyes_height)
        result.eyes = eyes
        result.add(eyes)
        result.move_to(self.get_grid_position(0, index))
        result.to_edge(UP, buff = LARGE_BUFF)
        return result

    def get_grid_position(self, i, j):
        x = VGroup(*self.v_lines[j:j+2]).get_center()[0]
        y = VGroup(*self.h_lines[i:i+2]).get_center()[1]
        return x*RIGHT + y*UP

    def get_requested_change_bubble(self, example_mob):
        change = self.get_random_decimal()
        words = OldTexText("Change by")
        change.next_to(words, RIGHT)
        change.save_state()
        content = VGroup(words, change)

        bubble = SpeechBubble(height = 1.5, width = 3)
        bubble.add_content(content)
        group = VGroup(bubble, content)
        group.shift(
            example_mob.get_right() + SMALL_BUFF*RIGHT \
            -bubble.get_corner(DOWN+LEFT)
        )

        return VGroup(bubble, words), change

    def get_random_decimal(self):
        return self.get_colored_decimal(
            0.3*(random.random() - 0.5)
        )

    def get_colored_decimal(self, number):
        result = DecimalNumber(number)
        if result.number > 0:
            plus = OldTex("+")
            plus.next_to(result, LEFT, SMALL_BUFF)
            result.add_to_back(plus)
            result.set_color(BLUE)
        else:
            result.set_color(RED)
        return result

    def get_look_at_anims(self, mob):
        return [eyes.look_at_anim(mob) for eyes in self.all_eyes]

    def blink(self, n):
        for x in range(n):
            self.play(random.choice(self.all_eyes).blink_anim())
