# ==============================================================================
# Scene:      SimpleGraphOfTwoToT
# Source:     videos/_2017/eoc/chapter5.py (lines 569-592)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleGraphOfTwoToT.py SimpleGraphOfTwoToT -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GraphOfTwoToT(GraphScene):
    CONFIG = {
        "x_axis_label" : "$t$",
        "y_axis_label" : "$M$",
        "x_labeled_nums" : list(range(1, 7)),
        "y_labeled_nums" : list(range(8, 40, 8)),
        "x_max" : 6,
        "y_min" : 0,
        "y_max" : 32,
        "y_tick_frequency" : 2,
        "graph_origin" : 2.5*DOWN + 5*LEFT,
    }
    def construct(self):
        self.setup_axes()
        example_t = 3
        graph = self.get_graph(lambda t : 2**t, color = BLUE_C)
        self.graph = graph
        graph_label = self.get_graph_label(
            graph, "M(t) = 2^t",
            direction = LEFT,
        )
        label_group = self.get_label_group(example_t)
        v_line, brace, height_label, ss_group, slope_label = label_group
        self.animate_secant_slope_group_change(
            ss_group,
            target_dx = 1,
            run_time = 0
        )
        self.remove(ss_group)

        #Draw graph and revert to tangent
        self.play(ShowCreation(graph))
        self.play(Write(graph_label))
        self.wait()
        self.play(Write(ss_group))
        self.wait()
        for target_dx in 0.01, 1, 0.01:
            self.animate_secant_slope_group_change(
                ss_group,
                target_dx = target_dx
            )
            self.wait()

        #Mark up with values

        self.play(ShowCreation(v_line))
        self.play(
            GrowFromCenter(brace),
            Write(height_label, run_time = 1)
        )
        self.wait()
        self.play(
            FadeIn(
                slope_label, 
                run_time = 4,
                lag_ratio = 0.5
            ),
            ReplacementTransform(
                height_label.copy(),
                slope_label.get_part_by_tex("2^")
            )
        )
        self.wait()

        #Vary value
        threes = VGroup(height_label[1], slope_label[2][1])
        ts = VGroup(*[
            OldTex("t").set_color(YELLOW).scale(0.75).move_to(three)
            for three in threes
        ])
        self.play(Transform(threes, ts))

        alt_example_t = example_t+1
        def update_label_group(group, alpha):
            t = interpolate(example_t, alt_example_t, alpha)
            new_group = self.get_label_group(t)
            Transform(group, new_group).update(1)
            for t, three in zip(ts, threes):
                t.move_to(three)
            Transform(threes, ts).update(1)
            return group

        self.play(UpdateFromAlphaFunc(
            label_group, update_label_group,
            run_time = 3,
        ))
        self.play(UpdateFromAlphaFunc(
            label_group, update_label_group,
            run_time = 3,
            rate_func = lambda t : 1 - 1.5*smooth(t)
        ))

    def get_label_group(self, t):
        graph = self.graph

        v_line = self.get_vertical_line_to_graph(
            t, graph,
            color = YELLOW,
        )
        brace = Brace(v_line, RIGHT)
        height_label = brace.get_text("$2^%d$"%t)

        ss_group = self.get_secant_slope_group(
            t, graph, dx = 0.01,
            df_label = "dM",
            dx_label = "dt",
            dx_line_color = GREEN,
            secant_line_color = RED,
        )
        slope_label = OldTex(
            "\\text{Slope}", "=", 
            "2^%d"%t,
            "(%.7f\\dots)"%np.log(2)
        )
        slope_label.next_to(
            ss_group.secant_line.point_from_proportion(0.65),
            DOWN+RIGHT,
            buff = 0
        )
        slope_label.set_color_by_tex("Slope", RED)
        return VGroup(
            v_line, brace, height_label,
            ss_group, slope_label
        )


class SimpleGraphOfTwoToT(GraphOfTwoToT):
    CONFIG = {
        "x_axis_label" : "",
        "y_axis_label" : "",
    }
    def construct(self):
        self.setup_axes()
        func = lambda t : 2**t
        graph = self.get_graph(func)
        line_pairs = VGroup()
        for x in 1, 2, 3, 4, 5:
            point = self.coords_to_point(x, func(x))
            x_axis_point = self.coords_to_point(x, 0)
            y_axis_point = self.coords_to_point(0, func(x))
            line_pairs.add(VGroup(
                DashedLine(x_axis_point, point),
                DashedLine(y_axis_point, point),
            ))


        self.play(ShowCreation(graph, run_time = 2))
        for pair in line_pairs:
            self.play(ShowCreation(pair))
        self.wait()
