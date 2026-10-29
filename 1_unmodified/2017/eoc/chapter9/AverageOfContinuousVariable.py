# ==============================================================================
# Scene:      AverageOfContinuousVariable
# Source:     videos/_2017/eoc/chapter9.py (lines 21-72)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AverageOfContinuousVariable.py AverageOfContinuousVariable -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AverageOfContinuousVariable(GraphScene):
    CONFIG = {
        "bounds" : [1, 7],
        "bound_colors" : [RED, GREEN],
    }
    def construct(self):
        self.setup_axes()
        graph = self.get_graph(
            lambda x : 0.1*x*(x-3)*(x-6) + 4
        )
        graph_label = self.get_graph_label(graph, "f(x)")
        boundary_lines = self.get_vertical_lines_to_graph(
            graph, *self.bounds, num_lines = 2,
            line_class = DashedLine
        )
        for line, color in zip(boundary_lines, self.bound_colors):
            line.set_color(color)
        v_line = self.get_vertical_line_to_graph(
            self.bounds[0], graph, color = YELLOW,
        )

        question = OldTexText(
            "What is the average \\\\ value of $f(x)$?"
        )
        question.next_to(boundary_lines, UP)

        self.play(ShowCreation(graph), Write(graph_label))
        self.play(ShowCreation(boundary_lines))
        self.play(FadeIn(
            question,
            run_time = 2,
            lag_ratio = 0.5,
        ))
        self.play(ShowCreation(v_line))
        for bound in reversed(self.bounds):
            self.play(self.get_v_line_change_anim(
                v_line, graph, bound, 
                run_time = 3,
            ))
            self.wait()
        self.wait()

    def get_v_line_change_anim(self, v_line, graph, target_x, **kwargs):
        start_x = self.x_axis.point_to_number(v_line.get_bottom())
        def update(v_line, alpha):
            new_x = interpolate(start_x, target_x, alpha)
            v_line.put_start_and_end_on(
                self.coords_to_point(new_x, 0),
                self.input_to_graph_point(new_x, graph)
            )
            return v_line
        return UpdateFromAlphaFunc(v_line, update, **kwargs)
