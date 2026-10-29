# ==============================================================================
# Scene:      ExampleMultivariableFunction
# Source:     videos/_2018/alt_calc.py (lines 896-912)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExampleMultivariableFunction.py ExampleMultivariableFunction -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class ExampleMultivariableFunction(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": False,
        "show_coordinates": True,
    }

    def construct(self):
        def example_function(point):
            x, y, z = point
            return np.array([
                x + np.sin(y),
                y + np.sin(x),
                0
            ])
        self.wait()
        self.apply_nonlinear_transformation(example_function, run_time=5)
        self.wait()
