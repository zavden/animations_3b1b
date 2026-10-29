# ==============================================================================
# Scene:      HyperSlinky
# Source:     videos/outside_videos/gifs.py (lines 4-17)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HyperSlinky.py HyperSlinky -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HyperSlinky(Scene):
    def construct(self):
        self.play(
            ApplyPointwiseFunction(
                lambda x_y_z: (1 + x_y_z[1]) * np.array((
                    np.cos(2 * np.pi * x_y_z[0]),
                    np.sin(2 * np.pi * x_y_z[0]),
                    x_y_z[2]
                )),
                NumberPlane().prepare_for_nonlinear_transform(),
                rate_func=there_and_back,
                run_time=10,
            )
        )
