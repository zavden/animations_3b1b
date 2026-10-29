# ==============================================================================
# Scene:      ConfusedAtParabolicData
# Source:     videos/_2017/fractal_dimension.py (lines 2191-2207)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConfusedAtParabolicData.py ConfusedAtParabolicData -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PlotDiskBoxCounting(GraphScene):
    CONFIG = {
        "x_axis_label" : "Scaling factor",
        "y_axis_label" : "Number of boxes \\\\ touched",
        "x_labeled_nums" : [],
        "y_labeled_nums" : [],
        "x_min" : 0,
        "y_min" : 0,
        "y_max" : 30,
        "func" : lambda x : 0.5*x**2,
        "func_label" : "f(x) = cx^2",
    }
    def construct(self):
        self.plot_points()
        self.describe_better_fit()

    def plot_points(self):
        self.setup_axes()
        self.graph_function(self.func)
        self.remove(self.graph)

        data_points = [
            self.input_to_graph_point(x) + ((random.random()-0.5)/x)*UP
            for x in np.arange(2, 10, 0.5)
        ]
        data_dots = VGroup(*[
            Dot(point, radius = 0.05, color = YELLOW)
            for point in data_points
        ])

        self.play(ShowCreation(data_dots))
        self.wait()
        self.play(ShowCreation(self.graph))
        self.label_graph(
            self.graph,
            self.func_label,
            direction = RIGHT+DOWN,
            buff = SMALL_BUFF,
            color = WHITE,
        )
        self.wait()

    def describe_better_fit(self):
        words = OldTexText("Better fit at \\\\ higher inputs")
        arrow = Arrow(2*LEFT, 2*RIGHT)
        arrow.next_to(self.x_axis_label_mob, UP)
        arrow.shift(2*LEFT)
        words.next_to(arrow, UP)

        self.play(ShowCreation(arrow))
        self.play(Write(words))
        self.wait(2)


class ConfusedAtParabolicData(PlotDiskBoxCounting):
    CONFIG = {
        "func" : lambda x : 0.5*x**1.6,
        "func_label" : "f(x) = cx^{1.21}",
    }

    def construct(self):
        self.plot_points()
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)
        randy.shift(RIGHT)

        self.play(FadeIn(randy))
        self.play(randy.change_mode, "confused")
        self.play(randy.look_at, self.x_axis_label_mob)
        self.play(Blink(randy))
        self.wait(2)
