# ==============================================================================
# Scene:      ConvolutionalNetworkPreview
# Source:     videos/_2017/nn/part2.py (lines 3448-3487)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/network.py, _2017/nn/part1.py
#
# Run from this folder:
#     manimgl ConvolutionalNetworkPreview.py ConvolutionalNetworkPreview -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#   - Inlined network.py: data files (image_map, pretrained weights) live in the bundled nn/ folder next to the scene.
#   - Pickle data files must be opened in binary mode in Python 3.
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
import pickle
# Third-party libraries
import numpy as np
import warnings
# CHANGE: Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
import sys, os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # CL17-B
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


class PixelsFromVect(PixelsAsSquares):
    def __init__(self, vect, **kwargs):
        PixelsAsSquares.__init__(self,
            ImageMobject(layer_to_image_array(vect)),
            **kwargs
        )



# ----- From _2017/nn/part2.py -----

class ConvolutionalNetworkPreview(Scene):
    def construct(self):
        vect = get_organized_images()[9][0]
        image = PixelsFromVect(vect)
        image.set_stroke(width = 1)
        image.set_height(FRAME_HEIGHT - 1)
        self.add(image)

        kernels = [
            PixelsFromVect(np.zeros(16))
            for x in range(2)
        ]
        for i, pixel in enumerate(kernels[0]):
            x = i%4
            y = i//4
            if x == y:
                pixel.set_fill(BLUE, 1)
            elif abs(x - y) == 1:
                pixel.set_fill(BLUE, 0.5)
        for i, pixel in enumerate(kernels[1]):
            x = i%4
            if x == 1:
                pixel.set_fill(BLUE, 1)
            elif x == 2:
                pixel.set_fill(RED, 1)
        for kernel in kernels:
            kernel.set_stroke(width = 1)
            kernel.scale(image[0].get_height()/kernel[0].get_height())
            kernel.add(SurroundingRectangle(
                kernel, color = YELLOW, buff = 0
            ))
            self.add(kernel)
            for i, pixel in enumerate(image):
                x = i%28
                y = i//28
                if x > 24 or y > 24:
                    continue
                kernel.move_to(pixel, UP+LEFT)
                self.wait(self.frame_duration)
            self.remove(kernel)
