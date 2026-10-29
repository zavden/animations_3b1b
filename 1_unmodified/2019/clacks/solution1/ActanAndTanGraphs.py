# ==============================================================================
# Scene:      ActanAndTanGraphs
# Source:     videos/_2019/clacks/solution1.py (lines 2520-2602)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ActanAndTanGraphs.py ActanAndTanGraphs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ActanAndTanGraphs(GraphScene):
    CONFIG = {
        "x_min": -PI / 8,
        "x_max": 5 * PI / 8,
        "y_min": -PI / 8,
        "y_max": 4 * PI / 8,
        "x_tick_frequency": PI / 8,
        "x_leftmost_tick": -PI / 8,
        "y_tick_frequency": PI / 8,
        "y_leftmost_tick": -PI / 8,
        "x_axis_width": 10,
        "y_axis_height": 7,
        "graph_origin": 2.5 * DOWN + 5 * LEFT,
        "num_graph_anchor_points": 500,
    }

    def construct(self):
        self.setup_axes()
        axes = self.axes
        labels = VGroup(
            OldTex("\\pi / 8"),
            OldTex("\\pi / 4"),
            OldTex("3\\pi / 8"),
            OldTex("\\pi / 2"),
        )
        for n, label in zip(it.count(1), labels):
            label.scale(0.75)
            label.next_to(self.coords_to_point(n * PI / 8, 0), DOWN)
            self.add(label)

        id_graph = self.get_graph(lambda x: x, x_max=1.5)
        arctan_graph = self.get_graph(np.arctan, x_max=1.5)
        tan_graph = self.get_graph(np.tan, x_max=1.5)
        graphs = VGroup(id_graph, arctan_graph, tan_graph)

        id_label = OldTex("f(x) = x")
        arctan_label = OldTex("\\arctan(x)")
        tan_label = OldTex("\\tan(x)")
        labels = VGroup(id_label, arctan_label, tan_label)
        for label, graph in zip(labels, graphs):
            label.match_color(graph)
            label.next_to(graph.get_points()[-1], RIGHT)
            if label.get_bottom()[1] > FRAME_HEIGHT / 2:
                label.next_to(graph.point_from_proportion(0.75), LEFT)

        arctan_x_tracker = ValueTracker(3 * PI / 8)
        arctan_v_line = always_redraw(
            lambda: self.get_vertical_line_to_graph(
                arctan_x_tracker.get_value(),
                arctan_graph,
                line_class=DashedLine,
                color=WHITE,
            )
        )
        tan_x_tracker = ValueTracker(2 * PI / 8)
        tan_v_line = always_redraw(
            lambda: self.get_vertical_line_to_graph(
                tan_x_tracker.get_value(),
                tan_graph,
                line_class=DashedLine,
                color=WHITE,
            )
        )

        self.add(axes)
        self.play(
            ShowCreation(id_graph),
            Write(id_label)
        )
        self.play(
            ShowCreation(arctan_graph),
            Write(arctan_label)
        )
        self.add(arctan_v_line)
        self.play(arctan_x_tracker.set_value, 0, run_time=2)
        self.wait()
        self.play(
            TransformFromCopy(arctan_graph, tan_graph),
            TransformFromCopy(arctan_label, tan_label),
        )
        self.add(tan_v_line)
        self.play(tan_x_tracker.set_value, 0, run_time=2)
        self.wait()
