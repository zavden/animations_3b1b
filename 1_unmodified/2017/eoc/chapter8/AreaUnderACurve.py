# ==============================================================================
# Scene:      AreaUnderACurve
# Source:     videos/_2017/eoc/chapter8.py (lines 1440-1470)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AreaUnderACurve.py AreaUnderACurve -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AreaUnderACurve(GraphScene):
    CONFIG = {
        "y_max" : 4,
        "y_min" : 0,
        "num_iterations" : 7
    }
    def construct(self):
        self.setup_axes()
        graph = self.get_graph(self.func)
        rect_list = self.get_riemann_rectangles_list(
            graph, self.num_iterations
        )
        VGroup(*rect_list).set_fill(opacity = 0.8)
        rects = rect_list[0]

        self.play(ShowCreation(graph))
        self.play(Write(rects))
        for new_rects in rect_list[1:]:
            rects.align_family(new_rects)
            for every_other_rect in rects[::2]:
                every_other_rect.set_fill(opacity = 0)
            self.play(Transform(
                rects, new_rects,
                run_time = 2,
                lag_ratio = 0.5
            ))
        self.wait()


    def func(self, x):
        return np.sin(x) + 1
