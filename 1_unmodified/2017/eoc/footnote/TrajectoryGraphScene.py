# ==============================================================================
# Scene:      TrajectoryGraphScene
# Source:     videos/_2017/eoc/footnote.py (lines 660-676)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TrajectoryGraphScene.py TrajectoryGraphScene -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TrajectoryGraphScene(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_max" : 10,
        "x_axis_label" : "t",
        "y_axis_label" : "s",
        # "func" : lambda x : 10*smooth(x/10.0),
        "func" : lambda t : 10*bezier([0, 0, 0, 1, 1, 1])(t/10.0),
        "color" : BLUE,
    }
    def construct(self):
        self.setup_axes()
        self.graph = self.get_graph(
            self.func,
            color = self.color
        )
        self.add(self.graph)
