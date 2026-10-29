# ==============================================================================
# Scene:      SumRule
# Source:     videos/_2017/eoc/chapter4.py (lines 304-665)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SumRule.py SumRule -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 division gave an int-like count; np.linspace needs an int
#   - Python 2 integer division used as list index
# ==============================================================================

from manim_imports_ext import *

SINE_COLOR = BLUE


X_SQUARED_COLOR = GREEN


SUM_COLOR = YELLOW


class SumRule(GraphScene):
    CONFIG = {
        "x_labeled_nums" : [],
        "y_labeled_nums" : [],
        "y_axis_label" : "",
        "x_max" : 4,
        "x_axis_width" : FRAME_WIDTH,
        "y_max" : 3,
        "graph_origin" : 2.5*DOWN + 2.5*LEFT,
        "graph_label_x_value" : 1.5,
        "example_input" : 0.5,
        "example_input_string" : "0.5",
        "dx" : 0.05,
        "v_lines_x_min" : -1,
        "v_lines_x_max" : 2,
        "graph_scale_factor" : 2,
        "tex_scale_factor" : 0.8,
    }
    def construct(self):
        self.write_function()
        self.add_graphs()
        self.zoom_in_on_graph()
        self.show_example_stacking()
        self.show_df()
        self.expand_derivative()

    def write_function(self):
        func_mob = OldTex("f(x)", "=", "\\sin(x)", "+", "x^2")
        func_mob.scale(self.tex_scale_factor)
        func_mob.set_color_by_tex("f(x)", SUM_COLOR)
        func_mob.set_color_by_tex("\\sin(x)", SINE_COLOR)
        func_mob.set_color_by_tex("x^2", X_SQUARED_COLOR)
        func_mob.to_corner(UP+LEFT)
        self.add(func_mob)

        self.func_mob = func_mob

    def add_graphs(self):
        self.setup_axes()
        sine_graph = self.get_graph(np.sin, color = SINE_COLOR)
        parabola = self.get_graph(lambda x : x**2, color = X_SQUARED_COLOR)
        sum_graph = self.get_graph(
            lambda x : np.sin(x) + x**2, 
            color = SUM_COLOR
        )
        sine_label = self.get_graph_label(
            sine_graph, "\\sin(x)",
            x_val = self.graph_label_x_value,
            direction = UP+RIGHT,
            buff = 0,
        )
        sine_label.scale(self.tex_scale_factor)
        parabola_label = self.get_graph_label(
            parabola, "x^2", x_val = self.graph_label_x_value,
        )
        parabola_label.scale(self.tex_scale_factor)

        graphs = VGroup(sine_graph, parabola)
        labels = VGroup(sine_label, parabola_label)
        for label in labels:
            label.add_background_rectangle()

        for graph, label in zip(graphs, labels):
            self.play(
                ShowCreation(graph),
                Write(label)
            )
        self.wait()

        # CHANGE: Python 2 division gave an int-like count; np.linspace needs an int
        num_lines = int((self.v_lines_x_max-self.v_lines_x_min)/self.dx)
        sine_v_lines, parabox_v_lines = v_line_sets = [
            self.get_vertical_lines_to_graph(
                graph, 
                x_min = self.v_lines_x_min,
                x_max = self.v_lines_x_max, 
                num_lines = num_lines,
                stroke_width = 2
            )
            for graph in graphs
        ]
        sine_v_lines.shift(0.02*RIGHT)
        for v_lines in v_line_sets:
            self.play(ShowCreation(v_lines), Animation(labels))
        self.wait()
        self.play(*it.chain(
            [
                ApplyMethod(l2.move_to, l1.get_top(), DOWN)
                for l1, l2, in zip(*v_line_sets)
            ],
            [graph.fade for graph in graphs],
            [Animation(labels)]
        ))
        self.wait()

        self.play(ShowCreation(sum_graph))
        self.wait()

        self.sum_graph = sum_graph
        self.parabola = parabola
        self.sine_graph = sine_graph
        self.graph_labels = labels
        self.v_line_sets = v_line_sets

    def zoom_in_on_graph(self):
        graph_parts = VGroup(
            self.axes, 
            self.sine_graph, self.parabola, self.sum_graph,
            *self.v_line_sets
        )
        graph_parts.remove(self.func_mob, *self.graph_labels)
        graph_parts.generate_target()
        self.graph_labels.generate_target()
        for mob in graph_parts, self.graph_labels:
            mob.target.scale(
                self.graph_scale_factor, 
                about_point = self.graph_origin,
            )
        for mob in self.graph_labels.target:
            mob.scale(
                1./self.graph_scale_factor,
                about_point = mob.get_bottom()
            )
            mob.shift_onto_screen()
        self.play(*list(map(MoveToTarget, [
            graph_parts, self.graph_labels
        ])))
        self.wait()

    def show_example_stacking(self):
        v_line_sets = self.v_line_sets
        num_lines = len(v_line_sets[0])
        example_v_lines, nudged_v_lines = [
            VGroup(*[v_lines[index] for v_lines in v_line_sets])
            # CHANGE: Python 2 integer division used as list index
            for index in (num_lines//2, num_lines//2+1)
        ]
        for line in nudged_v_lines:
            line.save_state()
        sine_lines, parabola_lines = [
            VGroup(example_v_lines[i], nudged_v_lines[i])
            for i in (0, 1)
        ]
        faders = VGroup(*[line for line in it.chain(*v_line_sets) if line not in example_v_lines])
        label_groups = []
        for line, tex, vect in zip(sine_lines, ["", "+dx"], [LEFT, RIGHT]):
            dot = Dot(line.get_bottom(), radius = 0.03, color = YELLOW)
            label = OldTex(
                "x=" + str(self.example_input) + tex
            )
            label.next_to(dot, DOWN+vect, buff = MED_LARGE_BUFF)
            arrow = Arrow(
                label.get_corner(UP-vect), dot,
                buff = SMALL_BUFF,
                color = WHITE,
                tip_length = 0.1
            )
            label_groups.append(VGroup(label, arrow, dot))

        line_tex_direction_triplets = [
            (sine_lines[0], "\\sin(0.5)", LEFT),
            (sine_lines[1], "\\sin(0.5+dx)", RIGHT),
            (parabola_lines[0], "(0.5)^2", LEFT),
            (parabola_lines[1], "(0.5+dx)^2", RIGHT),
        ]
        for line, tex, direction in line_tex_direction_triplets:
            line.brace = Brace(
                line, direction,
                buff = SMALL_BUFF,
                min_num_quads = 2,
            )
            line.brace.set_color(line.get_color())
            line.brace.add_background_rectangle()
            line.brace_text = line.brace.get_text("$%s$"%tex)
            line.brace_text.scale(
                self.tex_scale_factor,
                about_point = line.brace_text.get_edge_center(-direction)
            )
            line.brace_text.add_background_rectangle()
            line.brace_anim = MaintainPositionRelativeTo(
                VGroup(line.brace, line.brace_text), line
            )

        ##Look at example lines
        self.play(
            example_v_lines.set_stroke, None, 4,
            faders.fade,
            Animation(self.graph_labels),
            Write(label_groups[0]),
        )
        for line in example_v_lines:
            line.save_state()
        self.wait()
        self.play(
            GrowFromCenter(sine_lines[0].brace),
            Write(sine_lines[0].brace_text),
        )
        self.wait()
        self.play(
            sine_lines[0].shift, UP+4*LEFT,
            sine_lines[0].brace_anim,
            parabola_lines[0].move_to, sine_lines[0], DOWN
        )
        self.wait()
        parabola_lines[0].brace_anim.update(1)
        self.play(
            GrowFromCenter(parabola_lines[0].brace),
            Write(parabola_lines[0].brace_text),
        )
        self.wait()
        self.play(*it.chain(*[
            [line.restore, line.brace_anim]
            for line in example_v_lines
        ]))

        ## Nudged_lines
        self.play(
            Write(label_groups[1]),
            *it.chain(*[
                [line.restore, line.set_stroke, None, 4]
                for line in nudged_v_lines
            ])
        )
        self.wait()
        for line in nudged_v_lines:
            self.play(
                GrowFromCenter(line.brace),
                Write(line.brace_text)
            )
        self.wait()

        self.sine_lines = sine_lines
        self.parabola_lines = parabola_lines

    def show_df(self):
        sine_lines = self.sine_lines
        parabola_lines = self.parabola_lines

        df, equals, d_sine, plus, d_x_squared = deriv_mob = OldTex(
            "df", "=", "d(\\sin(x))", "+", "d(x^2)"
        )
        df.set_color(SUM_COLOR)
        d_sine.set_color(SINE_COLOR)
        d_x_squared.set_color(X_SQUARED_COLOR)
        deriv_mob.scale(self.tex_scale_factor)
        deriv_mob.next_to(
            self.func_mob, DOWN, 
            buff = MED_LARGE_BUFF, 
            aligned_edge = LEFT
        )
        for submob in deriv_mob:
            submob.add_to_back(BackgroundRectangle(submob))

        df_lines = self.show_difference(parabola_lines, df, equals)
        self.wait()
        self.play(FadeOut(df_lines))
        self.play(
            parabola_lines[0].shift,
            (parabola_lines[1].get_bottom()[1]-parabola_lines[0].get_bottom()[1])*UP,
            parabola_lines[0].brace_anim
        )
        d_sine_lines = self.show_difference(sine_lines, d_sine, plus)
        d_x_squared_lines = self.show_difference(parabola_lines, d_x_squared, VGroup())
        self.wait()

        self.deriv_mob = deriv_mob
        self.d_sine_lines = d_sine_lines
        self.d_x_squared_lines = d_x_squared_lines

    def show_difference(self, v_lines, target_tex, added_tex):
        distance = v_lines[1].get_top()[1]-v_lines[0].get_top()[1]
        h_lines = VGroup(*[
            DashedLine(ORIGIN, 2*RIGHT, stroke_width = 3)
            for x in range(2)
        ])
        h_lines.arrange(DOWN, buff = distance)
        h_lines.move_to(v_lines[1].get_top(), UP+RIGHT)

        brace = Brace(h_lines, LEFT)
        brace_text = target_tex.copy()
        brace_text.next_to(brace, LEFT)

        self.play(ShowCreation(h_lines))
        self.play(GrowFromCenter(brace), Write(brace_text))
        self.wait()
        self.play(
            ReplacementTransform(brace_text.copy(), target_tex),
            Write(added_tex)
        )
        return VGroup(h_lines, brace, brace_text)

    def expand_derivative(self):
        expanded_deriv = OldTex(
            "df", "=", "\\cos(x)", "\\,dx", "+", "2x", "\\,dx"
        )
        expanded_deriv.set_color_by_tex("df", SUM_COLOR)
        VGroup(*expanded_deriv[2:4]).set_color(SINE_COLOR)
        VGroup(*expanded_deriv[5:7]).set_color(X_SQUARED_COLOR)
        expanded_deriv.scale(self.tex_scale_factor)
        expanded_deriv.next_to(
            self.deriv_mob, DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        background_rect = BackgroundRectangle(expanded_deriv)

        rearranged_deriv = OldTex(
            "{df \\over", "dx}", "=", "\\cos(x)", "+", "2x"
        )
        rearranged_deriv[0].set_color(SUM_COLOR)
        rearranged_deriv[3].set_color(SINE_COLOR)
        rearranged_deriv[5].set_color(X_SQUARED_COLOR)
        rearranged_deriv.scale(self.tex_scale_factor)
        rearranged_deriv.move_to(expanded_deriv, UP+LEFT)
        deriv_target_indices = [0, 2, 3, 1, 4, 5, 1]

        self.play(
            FadeIn(
                background_rect, 
                rate_func = squish_rate_func(smooth, 0.6, 1)
            ),
            Write(expanded_deriv)
        )
        self.wait()

        tex_group_pairs = [
            ("\\cos(0.5)dx", self.d_sine_lines),
            ("2(0.5)dx", self.d_x_squared_lines),
        ]
        def indicate(mob):
            self.play(
                mob.set_color, YELLOW,
                mob.scale, 1.2,
                rate_func = there_and_back
            )
        for tex, group in tex_group_pairs:
            old_label = group[-1]
            new_label = OldTex(tex)
            pre_dx = VGroup(*new_label[:-2])
            dx = VGroup(*new_label[-2:])
            new_label.add_background_rectangle()
            new_label.scale(self.tex_scale_factor)
            new_label.move_to(old_label, RIGHT)
            new_label.set_color(old_label.get_color())

            self.play(FocusOn(old_label))
            indicate(old_label)
            self.wait()
            self.play(FadeOut(old_label))
            self.play(FadeIn(new_label))
            self.wait()
            indicate(dx)
            self.wait()
            indicate(pre_dx)
            self.wait()
        self.wait()
        self.play(*[
            Transform(
                expanded_deriv[i], rearranged_deriv[j],
                path_arc = -np.pi/2
            )
            for i, j in enumerate(deriv_target_indices)
        ])
        self.wait()
