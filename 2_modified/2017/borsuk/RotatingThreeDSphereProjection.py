# ==============================================================================
# Scene:      RotatingThreeDSphereProjection
# Source:     videos/_2017/borsuk.py (lines 2607-2623)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RotatingThreeDSphereProjection.py RotatingThreeDSphereProjection -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Scene.repeat_frames (Cairo: append the frames again) does not exist; play the full rotation 4 more times
# ==============================================================================

from manim_imports_ext import *

class RotatingThreeDSphereProjection(Scene):
    CONFIG = {
        "camera_class" : ThreeDCamera,
    }
    def construct(self):
        sphere = VGroup(*[
            Circle(radius = np.sin(t)).shift(np.cos(t)*OUT)
            for t in np.linspace(0, np.pi, 20)
        ])
        sphere.set_stroke(BLUE, width = 2)
        # sphere.set_fill(BLUE, opacity = 0.1)

        self.play(Rotating(
            sphere, axis = RIGHT+OUT,
            run_time = 10
        ))
        # CHANGE: Scene.repeat_frames (Cairo: append the frames again) does not exist; play the full rotation 4 more times
        for _ in range(4):
            self.play(Rotating(sphere, axis = RIGHT+OUT, run_time = 10))
