# ==============================================================================
# Scene:      ZoomInOnBritain
# Source:     videos/_2017/fractal_dimension.py (lines 2474-2503)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ZoomInOnBritain.py ZoomInOnBritain -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
from functools import reduce

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


class ZoomInOnBritain(Scene):
    CONFIG = {
        "zoom_factor" : 1000
    }
    def construct(self):
        britain = Britain()
        fractalify(britain, order = 3, dimension = 1.21)
        anchors = britain.get_anchors()

        key_value = int(0.3*len(anchors))
        point = anchors[key_value]
        thinning_factor = 100
        num_neighbors_kept = 1000

        britain.set_points_as_corners(reduce(
            lambda a1, a2 : np.append(a1, a2, axis = 0),
            [
            anchors[:key_value-num_neighbors_kept:thinning_factor,:],
            anchors[key_value-num_neighbors_kept:key_value+num_neighbors_kept,:],
            anchors[key_value+num_neighbors_kept::thinning_factor,:],
            ]
        ))

        self.add(britain)
        self.wait()
        self.play(
            britain.scale, self.zoom_factor, point,
            run_time = 10
        )
        self.wait()
