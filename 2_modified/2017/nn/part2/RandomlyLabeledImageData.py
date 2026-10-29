# ==============================================================================
# Scene:      RandomlyLabeledImageData
# Source:     videos/_2017/nn/part2.py (lines 3489-3545)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/nn/part1.py
#
# Run from this folder:
#     manimgl RandomlyLabeledImageData.py RandomlyLabeledImageData -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Provide package `nn` (network.py with binary-mode pickle fix, mnist_loader.py reading a small synthetic MNIST stand-in) through data_files, since the original mnist.pkl.gz is not in the repo.
#   - Put the scene folder on sys.path so the bundled `nn` package (data_files) can be imported; manimgl does not add the script dir.
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2017/nn/nn_pkg/mnist_mini.npz (synthetic MNIST stand-in, built from the 100 real digits of image_map by make_nn_support.py)
#   - _lib/assets/raster_images/Adele.png (generic silhouette placeholder for the missing singer photo; copy of _lib/assets/generated/2017/nn/Adele.png made by make_adele_placeholder.py)
#
# Notes:
#   The 'Adele' picture is a generic silhouette placeholder (_lib/assets/raster_images/Adele.png); the other example pictures are third-party photos to be replaced for release (CODEX).
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

class RandomlyLabeledImageData(Scene):
    CONFIG = {
        "image_label_pairs" : [
            ("lion", "Lion"),
            ("Newton", "Genius"),
            ("Fork", "Fork"),
            ("Trilobite", "Trilobite"),
            ("Puppy", "Puppy"),
            ("Astrolabe", "Astrolabe"),
            ("Adele", "Songbird of \\\\ our generation"),
            ("Cow", "Cow"),
            ("Sculling", "Sculling"),
            ("Pierre_de_Fermat", "Tease"),
        ]
    }
    def construct(self):
        groups = Group()
        labels = VGroup()
        for i, (image_name, label_name) in enumerate(self.image_label_pairs):
            x = i//5
            y = i%5
            group = self.get_training_group(image_name, label_name)
            group.shift(4.5*LEFT + x*FRAME_X_RADIUS*RIGHT)
            group.shift(3*UP + 1.5*y*DOWN)
            groups.add(group)
            labels.add(group[-1])
        permutation = list(range(len(labels)))
        while any(np.arange(len(labels)) == permutation):
            random.shuffle(permutation)
        for label, i in zip(labels, permutation):
            label.generate_target()
            label.target.move_to(labels[i], LEFT)
            label.target.set_color(YELLOW)

        self.play(LaggedStartMap(
            FadeIn, groups,
            run_time = 3,
            lag_ratio = 0.3,
        ))
        self.wait()
        self.play(LaggedStartMap(
            MoveToTarget, labels, 
            run_time = 4,
            lag_ratio = 0.5,
            path_arc = np.pi/3,
        ))
        self.wait()

    def get_training_group(self, image_name, label_name):
        arrow = Vector(RIGHT, color = WHITE)
        image = ImageMobject(image_name)
        image.set_height(1.3)
        image.next_to(arrow, LEFT)
        label = OldTexText(label_name)
        label.next_to(arrow, RIGHT)
        group = Group(image, arrow, label)
        return group
