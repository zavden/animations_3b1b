# ==============================================================================
# Scene:      ProportionOfSphereInBox
# Source:     videos/_2017/highD.py (lines 3154-3199)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProportionOfSphereInBox.py ProportionOfSphereInBox -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProportionOfSphereInBox(GraphScene):
    CONFIG = {
        "x_axis_label" : "Dimension",
        "y_axis_label" : "",
        "y_max" : 1.5,
        "y_min" : 0,
        "y_tick_frequency" : 0.25,
        "y_labeled_nums" : np.linspace(0.25, 1, 4),
        "x_min" : 0,
        "x_max" : 50,
        "x_tick_frequency" : 5,
        "x_labeled_nums" : list(range(10, 50, 10)),
        "num_graph_anchor_points" : 100,
    }
    def construct(self):
        self.setup_axes()
        title = OldTexText(
            "Proportion of inner sphere \\\\ inside box"
        )
        title.next_to(self.y_axis, RIGHT, MED_SMALL_BUFF, UP)
        self.add(title)

        graph = self.get_graph(lambda x : np.exp(0.1*(9-x)))
        max_y = self.coords_to_point(0, 1)[1]
        too_high = graph.get_points()[:,1] > max_y
        graph.get_points()[too_high, 1] = max_y

        footnote = OldTexText("""
            \\begin{flushleft}
            *I may or may not have used an easy-to-compute \\\\
            but not-totally-accurate curve here, due to \\\\
            the surprising difficulty in computing the real \\\\
            proportion :)
            \\end{flushleft}
        """,)
        footnote.scale(0.75)
        footnote.next_to(
            graph.point_from_proportion(0.3),
            UP+RIGHT, SMALL_BUFF
        )
        footnote.set_color(YELLOW)

        self.play(ShowCreation(graph, run_time = 5, rate_func=linear))
        self.wait()
        self.add(footnote)
        self.wait(0.25)
