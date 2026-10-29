# ==============================================================================
# Scene:      HeartOfCalculus
# Source:     videos/_2017/eoc/old_chapter1.py (lines 449-479)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HeartOfCalculus.py HeartOfCalculus -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HeartOfCalculus(GraphScene):
    CONFIG = {
        "x_labeled_nums" : [],
        "y_labeled_nums" : [],
    }
    def construct(self):
        self.setup_axes()
        self.graph_function(lambda x : 3*np.sin(x/2) + x)
        rect_sets = [
            self.get_riemann_rectangles(
                0, self.x_max, 1./(2**n), stroke_width = 1./(n+1)
            )
            for n in range(6)
        ]

        rects = rect_sets.pop(0)
        rects.save_state()
        rects.stretch_to_fit_height(0)
        rects.shift(
            (self.graph_origin[1] - rects.get_center()[1])*UP
        )
        self.play(
            rects.restore,
            lag_ratio = 0.5,
            run_time = 3
        )
        while rect_sets:
            self.play(
                Transform(rects, rect_sets.pop(0)),
                run_time = 2
            )
