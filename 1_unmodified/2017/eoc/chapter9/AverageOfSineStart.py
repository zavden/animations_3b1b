# ==============================================================================
# Scene:      AverageOfSineStart
# Source:     videos/_2017/eoc/chapter9.py (lines 92-181)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AverageOfSineStart.py AverageOfSineStart -w -m --fps 15
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


class AverageOfSineStart(AverageOfContinuousVariable):
    CONFIG = {
        "y_min" : -2, 
        "y_max" : 2,
        "x_min" : -1,
        "x_max" : 2.5*np.pi,
        "x_leftmost_tick" : 0,
        "x_tick_frequency" : np.pi/4,
        "x_axis_width" : 12,
        "graph_origin" : 5*LEFT,
        "x_label_scale_val" : 0.75,
        "func" : np.sin,
        "graph_color" : BLUE,
        "bounds" : [0, np.pi],
    }
    def construct(self):
        self.setup_axes()
        self.add_graph()
        self.ask_about_average()

    def add_graph(self, run_time = 1):
        graph = self.get_graph(self.func, color = self.graph_color)
        graph_label = self.get_graph_label(
            graph, "\\sin(x)",
            direction = UP
        )
        self.play(
            ShowCreation(graph),
            Write(graph_label),
            run_time = run_time
        )

        self.graph = graph
        self.graph_label = graph_label

    def ask_about_average(self):
        half_period_graph = self.get_graph_portion_between_bounds()
        question = OldTexText("Average height?")
        question.to_edge(UP)
        arrow = Arrow(question.get_bottom(), half_period_graph.get_top())
        midpoint = np.mean(self.bounds)
        v_line = self.get_vertical_line_to_graph(
            midpoint, self.graph,
            line_class = DashedLine,
            color = WHITE
        )

        self.play(FadeIn(half_period_graph))
        self.play(
            Write(question, run_time = 2),
            ShowCreation(arrow)
        )
        self.play(ShowCreation(v_line))
        for bound in self.bounds + [midpoint]:
            self.play(self.get_v_line_change_anim(
                v_line, self.graph, bound,
                run_time = 3
            ))

    #########

    def get_graph_portion_between_bounds(self):
        self.graph_portion_between_bounds = self.get_graph(
            self.func,
            x_min = self.bounds[0],
            x_max = self.bounds[1],
            color = YELLOW
        )
        return self.graph_portion_between_bounds

    def setup_axes(self):
        GraphScene.setup_axes(self)
        self.add_x_axis_labels()

    def add_x_axis_labels(self):
        labels_and_x_values = [
            ("\\pi/2", np.pi/2),
            ("\\pi", np.pi),
            ("3\\pi/2", 3*np.pi/2),
            ("2\\pi", 2*np.pi),
        ]
        self.x_axis_labels = VGroup()
        for label, x in labels_and_x_values:
            tex_mob = OldTex(label)
            tex_mob.scale(self.x_label_scale_val)
            tex_mob.move_to(
                self.coords_to_point(x, -3*self.x_axis.tick_size), 
            )
            self.add(tex_mob)
            self.x_axis_labels.add(tex_mob)
