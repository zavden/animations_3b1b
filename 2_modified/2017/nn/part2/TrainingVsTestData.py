# ==============================================================================
# Scene:      TrainingVsTestData
# Source:     videos/_2017/nn/part2.py (lines 330-423)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py
#
# Run from this folder:
#     manimgl TrainingVsTestData.py TrainingVsTestData -w -m --fps 15
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
import random
# Third-party libraries
import numpy as np
# CHANGE: Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
import sys, os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # CL17-B
from nn.mnist_loader import load_data_wrapper
import warnings
from nn.network import *


# ----- From _2017/nn/network.py -----

def layer_to_image_array(layer):
    w = int(np.ceil(np.sqrt(len(layer))))
    if len(layer) < w**2:
        layer = np.append(layer, np.zeros(w**2 - len(layer)))
    layer = layer.reshape((w, w))
    # return Image.fromarray((255*layer).astype('uint8'))
    return (255*layer).astype('int')



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



# ----- From _2017/nn/part2.py -----

def get_training_image_group(train_in, train_out):
    image = MNistMobject(train_in)
    image.set_height(1)
    arrow = Vector(RIGHT, color = BLUE, buff = 0)
    output = np.argmax(train_out)
    output_tex = OldTex(str(output)).scale(1.5)
    result = Group(image, arrow, output_tex)
    result.arrange(RIGHT)
    result.to_edge(UP)
    return result


class TrainingVsTestData(Scene):
    CONFIG = {
        "n_examples" : 10,
        "n_new_examples_shown" : 10,
    }
    def construct(self):
        self.initialize_data()
        self.introduce_all_data()
        self.subdivide_into_training_and_testing()
        self.scroll_through_much_data()

    def initialize_data(self):
        training_data, validation_data, test_data = load_data_wrapper()
        self.data = training_data
        self.curr_index = 0

    def get_examples(self):
        ci = self.curr_index
        self.curr_index += self.n_examples
        group = Group(*it.starmap(
            get_training_image_group,
            self.data[ci:ci+self.n_examples]
        ))
        group.arrange(DOWN)
        group.scale(0.5)
        return group

    def introduce_all_data(self):
        training_examples, test_examples = [
            self.get_examples() for x in range(2)
        ]

        training_examples.next_to(ORIGIN, LEFT)
        test_examples.next_to(ORIGIN, RIGHT)
        self.play(
            LaggedStartMap(FadeIn, training_examples),
            LaggedStartMap(FadeIn, test_examples),
        )

        self.training_examples = training_examples
        self.test_examples = test_examples

    def subdivide_into_training_and_testing(self):
        training_examples = self.training_examples
        test_examples = self.test_examples
        for examples in training_examples, test_examples:
            examples.generate_target()
        training_examples.target.shift(2*LEFT)
        test_examples.target.shift(2*RIGHT)

        train_brace = Brace(training_examples.target, LEFT)
        train_words = train_brace.get_text("Train on \\\\ these")
        test_brace = Brace(test_examples.target, RIGHT)
        test_words = test_brace.get_text("Test on \\\\ these")

        bools = [True]*(len(test_examples)-1) + [False]
        random.shuffle(bools)
        marks = VGroup()
        for is_correct, test_example in zip(bools, test_examples.target):
            if is_correct:
                mark = OldTex("\\checkmark")
                mark.set_color(GREEN)
            else:
                mark = OldTex("\\times")
                mark.set_color(RED)
            mark.next_to(test_example, LEFT)
            marks.add(mark)

        self.play(
            MoveToTarget(training_examples),
            GrowFromCenter(train_brace),
            FadeIn(train_words)
        )
        self.wait()
        self.play(
            MoveToTarget(test_examples),
            GrowFromCenter(test_brace),
            FadeIn(test_words)
        )
        self.play(Write(marks))
        self.wait()

    def scroll_through_much_data(self):
        training_examples = self.training_examples
        colors = color_gradient([BLUE, YELLOW], self.n_new_examples_shown)
        for color in colors:
            new_examples = self.get_examples()
            new_examples.move_to(training_examples)
            for train_ex, new_ex in zip(training_examples, new_examples):
                self.remove(train_ex)
                self.add(new_ex)
                new_ex[0][0].set_color(color)
                self.wait(1./30)
            training_examples = new_examples
