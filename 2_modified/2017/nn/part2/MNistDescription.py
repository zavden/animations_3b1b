# ==============================================================================
# Scene:      MNistDescription
# Source:     videos/_2017/nn/part2.py (lines 425-503)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py
#
# Run from this folder:
#     manimgl MNistDescription.py MNistDescription -w -m --fps 15
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

class MNistDescription(Scene):
    CONFIG = {
        "n_grids" : 5,
        "n_rows_per_grid" : 10,
        "n_cols_per_grid" : 8,
        "time_per_example" : 1./120,
    }
    def construct(self):
        title = OldTexText("MNIST Database")
        title.scale(1.5)
        title.set_color(BLUE)
        authors = OldTexText("LeCun, Cortes and Burges")
        authors.next_to(title, DOWN)
        link_words = OldTexText("(links in the description)")
        link_words.next_to(authors, DOWN, MED_LARGE_BUFF)
        arrows = VGroup(*[Vector(DOWN) for x in range(4)])
        arrows.arrange(RIGHT, buff = LARGE_BUFF)
        arrows.next_to(link_words, DOWN)
        arrows.set_color(BLUE)

        word_group = VGroup(title, authors, link_words, arrows)
        word_group.center()

        self.add(title, authors)
        self.play(
            Write(link_words, run_time = 2),
            LaggedStartMap(GrowArrow, arrows),
        )
        self.wait()

        training_data, validation_data, test_data = load_data_wrapper()
        epc = self.n_rows_per_grid*self.n_cols_per_grid
        training_data_groups = [
            training_data[i*epc:(i+1)*epc]
            for i in range(self.n_grids)
        ]

        for i, td_group in enumerate(training_data_groups):
            print(i)
            group = Group(*[
                self.get_digit_pair(v_in, v_out)
                for v_in, v_out in td_group
            ])
            group.arrange_in_grid(
                n_rows = self.n_rows_per_grid,
            )
            group.set_height(FRAME_HEIGHT - 1)
            if i == 0:
                self.play(
                    LaggedStartMap(FadeIn, group),
                    FadeOut(word_group),
                )
            else:
                pairs = list(zip(last_group, group))
                random.shuffle(pairs)
                time = 0
                for t1, t2 in pairs:
                    time += self.time_per_example
                    self.remove(t1)
                    self.add(t2)
                    if time > self.frame_duration:
                        self.wait(self.frame_duration)
                        time = 0
            last_group = group


    def get_digit_pair(self, v_in, v_out):
        tup = Group(*OldTex("(", "00", ",", "0", ")"))  # CHANGE: `Tex(` here is the NEW GL class (different piece splitting, ...
        tup.scale(2)
        # image = PixelsFromVect(v_in)
        # image.add(SurroundingRectangle(image, color = BLUE, buff = SMALL_BUFF))
        image = MNistMobject(v_in)
        label = OldTex(str(np.argmax(v_out)))
        image.replace(tup[1])
        tup.submobjects[1] = image
        label.replace(tup[3], dim_to_match = 1)
        tup.submobjects[3] = label

        return tup
