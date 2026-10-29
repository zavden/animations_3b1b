# ==============================================================================
# Scene:      OrganizeDataIntoMiniBatches
# Source:     videos/_2017/nn/part3.py (lines 1868-2010)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py
#
# Run from this folder:
#     manimgl OrganizeDataIntoMiniBatches.py OrganizeDataIntoMiniBatches -w -m --fps 15
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



# ----- From _2017/nn/part3.py -----

class OrganizeDataIntoMiniBatches(Scene):
    CONFIG = {
        "n_rows" : 5,
        "n_cols" : 12,
        "example_height" : 1,
        "random_seed" : 0,
    }
    def construct(self):
        self.seed_random_libraries()
        self.add_examples()
        self.shuffle_examples()
        self.divide_into_minibatches()
        self.one_step_per_batch()

    def seed_random_libraries(self):
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)

    def add_examples(self):
        examples = self.get_examples()
        self.arrange_examples_in_grid(examples)
        for example in examples:
            example.save_state()
        alt_order_examples = VGroup(*examples)
        for mob in examples, alt_order_examples:
            random.shuffle(mob.submobjects)
        self.arrange_examples_in_grid(examples)

        self.play(LaggedStartMap(
            FadeIn, alt_order_examples,
            lag_ratio = 0.2,
            run_time = 4
        ))
        self.wait()

        self.examples = examples

    def shuffle_examples(self):
        self.play(LaggedStartMap(
            ApplyMethod, self.examples,
            lambda m : (m.restore,),
            lag_ratio = 0.3,
            run_time = 3,
            path_arc = np.pi/3,
        ))
        self.wait()

    def divide_into_minibatches(self):
        examples = self.examples
        examples.sort(lambda p : -p[1])
        rows = Group(*[
            Group(*examples[i*self.n_cols:(i+1)*self.n_cols])
            for i in range(self.n_rows)
        ])

        mini_batches_words = OldTexText("``Mini-batches''")
        mini_batches_words.to_edge(UP)
        mini_batches_words.set_color(YELLOW)

        self.play(
            rows.space_out_submobjects, 1.5,
            rows.to_edge, UP, 1.5,
            Write(mini_batches_words, run_time = 1)
        )

        rects = VGroup(*[
            SurroundingRectangle(
                row, 
                stroke_width = 0,
                fill_color = YELLOW,
                fill_opacity = 0.25,
            )
            for row in rows
        ])
        self.play(LaggedStartMap(
            FadeIn, rects,
            lag_ratio = 0.7,
            rate_func = there_and_back
        ))
        self.wait()

        self.set_variables_as_attrs(rows, rects, mini_batches_words)

    def one_step_per_batch(self):
        rows = self.rows
        brace = Brace(rows[0], UP, buff = SMALL_BUFF)
        text = brace.get_text(
            "Compute gradient descent step (using backprop)",
            buff = SMALL_BUFF
        )
        def indicate_row(row):
            row.sort(lambda p : p[0])
            return LaggedStartMap(
                ApplyFunction, row,
                lambda row : (
                    lambda m : m.scale(0.75).set_color(YELLOW),
                    row
                ),
                rate_func = wiggle
            )

        self.play(
            FadeOut(self.mini_batches_words),
            GrowFromCenter(brace),
            Write(text, run_time = 2),
        )
        self.play(indicate_row(rows[0]))
        brace.add(text)
        for last_row, row in zip(rows, rows[1:-1]):
            self.play(
                last_row.shift, UP,
                brace.next_to, row, UP, SMALL_BUFF
            )
            self.play(indicate_row(row))
        self.wait()


    ###

    def get_examples(self):
        n_examples = self.n_rows*self.n_cols
        height = self.example_height
        training_data, validation_data, test_data = load_data_wrapper()
        return Group(*[
            MNistMobject(
                t[0],
                rect_kwargs = {"stroke_width" : 2}
            ).set_height(height)
            for t in training_data[:n_examples]
        ])
        # return Group(*[
        #     Square(
        #         color = BLUE, 
        #         stroke_width = 2
        #     ).set_height(height)
        #     for x in range(n_examples)
        # ])

    def arrange_examples_in_grid(self, examples):
        examples.arrange_in_grid(
            n_rows = self.n_rows,
            buff = SMALL_BUFF
        )
