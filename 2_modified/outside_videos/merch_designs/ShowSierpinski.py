# ==============================================================================
# Scene:      ShowSierpinski
# Source:     videos/outside_videos/merch_designs.py (lines 44-49)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowSierpinski.py ShowSierpinski -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - once_useful_constructs lives in _lib (before, in manimlib) and its fractals.py imports digest_config from manimlib.utils.dict_ops, where it no longer exists: the copy from dict_shenanigans is put there
#   - the fractals.py classes read order, etc. as class attributes, but Mobject.__init__ no longer accepts those kwargs
#   - before, scale() also scaled the stroke width (the widths 20, 15, 7 are meant for that); now it does not, so it is scaled by hand
# ==============================================================================

from manim_imports_ext import *
# CHANGE: once_useful_constructs lives in _lib (before, in manimlib) and its fractals.py imports digest_config from manimlib.utils.dict_ops, where it no longer exists: the copy from dict_shenanigans is put there
import manimlib.utils.dict_ops as _dict_ops
from once_useful_constructs.dict_shenanigans import digest_config as _digest_config
_dict_ops.digest_config = _digest_config
from once_useful_constructs.fractals import *

# CHANGE: the fractals.py classes read order, etc. as class attributes, but Mobject.__init__ no longer accepts those kwargs
def make_fractal(FractalClass, **attrs):
    return type(FractalClass.__name__, (FractalClass,), attrs)()

# Fractal posters
class ShowHilbertCurve(Scene):
    CONFIG = {
        "FractalClass": HilbertCurve,
        "orders": [3, 5, 7],
        "stroke_widths": [20, 15, 7],
    }

    def construct(self):
        curves = VGroup(*[
            make_fractal(
                self.FractalClass,
                order=order,
            ).scale(scale_factor)
            for order, scale_factor in zip(
                self.orders,
                np.linspace(1, 2, 3)
            )
        ])
        for curve, stroke_width in zip(curves, self.stroke_widths):
            curve.set_stroke(width=stroke_width)
        curves.arrange(DOWN, buff=LARGE_BUFF)
        # CHANGE: before, scale() also scaled the stroke width (the widths 20, 15, 7 are meant for that); now it does not, so it is scaled by hand
        height_ratio = (FRAME_HEIGHT - 1) / curves.get_height()
        curves.set_height(FRAME_HEIGHT - 1)
        for curve, stroke_width in zip(curves, self.stroke_widths):
            curve.set_stroke(width=stroke_width * height_ratio)
        self.add(*curves)


class FlippedSierpinski(Sierpinski):
    def __init__(self, *args, **kwargs):
        Sierpinski.__init__(self, *args, **kwargs)
        self.rotate(np.pi, RIGHT, about_point=ORIGIN)


class ShowSierpinski(ShowHilbertCurve):
    CONFIG = {
        "FractalClass": FlippedSierpinski,
        "orders": [3, 6, 9],
        "stroke_widths": [20, 15, 6],
    }
