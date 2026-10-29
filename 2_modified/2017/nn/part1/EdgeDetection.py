# ==============================================================================
# Scene:      EdgeDetection
# Source:     videos/_2017/nn/part1.py (lines 2090-2106)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EdgeDetection.py EdgeDetection -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
#
# Notes:
#   Uses cv2 (opencv-python-headless already in the venv). The lion photo (raster_images/Lion.jpg) is a third-party photo to be replaced for release (CODEX).
# ==============================================================================

import sys
import os.path
import cv2
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


DEFAULT_GAUSS_BLUR_CONFIG = {
    "ksize"  : (5, 5), 
    "sigmaX" : 10, 
    "sigmaY" : 10,
}


DEFAULT_CANNY_CONFIG = {
    "threshold1" : 100,
    "threshold2" : 200,
}


def get_edges(image_array):
    blurred = cv2.GaussianBlur(
        image_array, 
        **DEFAULT_GAUSS_BLUR_CONFIG
    )
    edges = cv2.Canny(
        blurred, 
        **DEFAULT_CANNY_CONFIG
    )
    return edges


class EdgeDetection(Scene):
    CONFIG = {
        "camera_config" : {"background_opacity" : 1}
    }
    def construct(self):
        lion = ImageMobject("Lion")
        edges_array = get_edges(lion.pixel_array)
        edges = ImageMobject(edges_array)
        group = Group(lion, edges)
        group.set_height(4)
        group.arrange(RIGHT)
        lion_copy = lion.copy()

        self.play(FadeIn(lion))
        self.play(lion_copy.move_to, edges)
        self.play(Transform(lion_copy, edges, run_time = 3))
        self.wait(2)
