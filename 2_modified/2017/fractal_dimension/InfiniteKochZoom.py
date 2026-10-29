# ==============================================================================
# Scene:      InfiniteKochZoom
# Source:     videos/_2017/fractal_dimension.py (lines 415-440)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl InfiniteKochZoom.py InfiniteKochZoom -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Scene.repeat_frames does not exist (neither in Cairo sep19/3feb nor GL): hold the last frame with wait()
# ==============================================================================

from manim_imports_ext import *

class InfiniteKochZoom(Scene):
    CONFIG = {
        "order" : 6,
        "left_point" : 3*LEFT,
    }
    def construct(self):
        small_curve = self.get_curve(self.order)
        larger_curve = self.get_curve(self.order + 1)
        larger_curve.scale(3, about_point = small_curve.get_points()[0])
        self.play(Transform(small_curve, larger_curve, run_time = 2))
        # CHANGE: Scene.repeat_frames does not exist (neither in Cairo sep19/3feb nor GL): hold the last frame with wait()
        self.wait()



    def get_curve(self, order):
        koch_curve = KochCurve(
            monochromatic = True,
            order = order,
            color = BLUE,
            stroke_width = 2,
        )
        koch_curve.set_width(18)
        koch_curve.shift(
            self.left_point - koch_curve.get_points()[0]
        )
        return koch_curve
