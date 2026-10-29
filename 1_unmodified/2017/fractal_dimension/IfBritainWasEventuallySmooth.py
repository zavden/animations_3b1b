# ==============================================================================
# Scene:      IfBritainWasEventuallySmooth
# Source:     videos/_2017/fractal_dimension.py (lines 2617-2629)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IfBritainWasEventuallySmooth.py IfBritainWasEventuallySmooth -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Britain(SVGMobject):
    CONFIG = {
        "file_name" : "Britain.svg",
        "stroke_width" : 0,
        "fill_color" : BLUE_D,
        "fill_opacity" : 1,
        "height" : 5,
        "mark_paths_closed" : True,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.set_points(self[0].get_points())
        self.submobjects = []
        self.set_height(self.height)
        self.center()


class IfBritainWasEventuallySmooth(Scene):
    def construct(self):
        britain = Britain()
        britain.make_smooth()
        point = britain.point_from_proportion(0.3)

        self.add(britain)
        self.wait()
        self.play(
            britain.scale, 200, point,
            run_time = 10
        )
        self.wait()
