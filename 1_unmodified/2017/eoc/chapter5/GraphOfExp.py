# ==============================================================================
# Scene:      GraphOfExp
# Source:     videos/_2017/eoc/chapter5.py (lines 1142-1224)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GraphOfExp.py GraphOfExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GraphOfExp(GraphScene):
    CONFIG = {
        "x_min" : -3,
        "x_max" : 3,
        "x_tick_frequency" : 1,
        "x_axis_label" : "t",
        "x_labeled_nums" : list(range(-3, 4)),
        "x_axis_width" : 11,
        "graph_origin" : 2*DOWN + LEFT,
        "example_inputs" : [1, 2],
        "small_dx" : 0.01,
    }
    def construct(self):
        self.setup_axes()
        self.show_slopes()

    def show_slopes(self):
        graph = self.get_graph(np.exp)
        graph_label = self.get_graph_label(
            graph, "e^t", direction = LEFT
        )
        graph_label.shift(MED_SMALL_BUFF*LEFT)

        start_input, target_input = self.example_inputs
        ss_group = self.get_secant_slope_group(
            start_input, graph,
            dx = self.small_dx,
            dx_label = "dt",
            df_label = "d(e^t)",
            secant_line_color = YELLOW,
        )
        v_lines = [
            self.get_vertical_line_to_graph(
                x, graph, 
                color = WHITE,
            )
            for x in self.example_inputs
        ]
        height_labels = [
            OldTex("e^%d"%x).next_to(vl, RIGHT, SMALL_BUFF)
            for vl, x in zip(v_lines, self.example_inputs)
        ]
        slope_labels = [
            OldTexText(
                "Slope = $e^%d$"%x
            ).next_to(vl.get_top(), UP+RIGHT).shift(0.7*RIGHT/x)
           for vl, x in zip(v_lines, self.example_inputs)
        ]

        self.play(
            ShowCreation(graph, run_time = 2),
            Write(
                graph_label, 
                rate_func = squish_rate_func(smooth, 0.5, 1),
            )
        )
        self.wait()
        self.play(*list(map(ShowCreation, ss_group)))
        self.play(Write(slope_labels[0]))
        self.play(ShowCreation(v_lines[0]))
        self.play(Write(height_labels[0]))
        self.wait(2)
        self.animate_secant_slope_group_change(
            ss_group,
            target_x = target_input,
            run_time = 2,
            added_anims = [
                Transform(
                    *pair, 
                    path_arc = np.pi/6,
                    run_time = 2
                )
                for pair in [
                    slope_labels,
                    v_lines,
                    height_labels,
                ]
            ]
        )
        self.wait(2)

        self.graph = graph
        self.ss_group = ss_group
