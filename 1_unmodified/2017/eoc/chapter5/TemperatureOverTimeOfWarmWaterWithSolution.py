# ==============================================================================
# Scene:      TemperatureOverTimeOfWarmWaterWithSolution
# Source:     videos/_2017/eoc/chapter5.py (lines 1718-1721)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TemperatureOverTimeOfWarmWaterWithSolution.py TemperatureOverTimeOfWarmWaterWithSolution -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TemperatureOverTimeOfWarmWater(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_axis_label" : "$t$",
        "y_axis_label" : "Temperature",
        "T_room" : 4,
        "include_solution" : False,
    }
    def construct(self):
        self.setup_axes()
        graph = self.get_graph(
            lambda t : 3*np.exp(-0.3*t) + self.T_room,
            color = RED
        )
        h_line = DashedLine(*[
            self.coords_to_point(x, self.T_room)
            for x in (self.x_min, self.x_max)
        ])
        T_room_label = OldTex("T_{\\text{room}}")
        T_room_label.next_to(h_line, LEFT)

        ode = OldTex(
            "\\frac{d\\Delta T}{dt} = -k \\Delta T"
        )
        ode.to_corner(UP+RIGHT)

        solution = OldTex(
            "\\Delta T(", "t", ") = e", "^{-k", "t}"
        )
        solution.next_to(ode, DOWN, MED_LARGE_BUFF)
        solution.set_color_by_tex("t", YELLOW)
        solution.set_color_by_tex("Delta", WHITE)

        delta_T_brace = Brace(graph, RIGHT)
        delta_T_label = OldTex("\\Delta T")
        delta_T_group = VGroup(delta_T_brace, delta_T_label)
        def update_delta_T_group(group):
            brace, label = group
            v_line = Line(
                graph.get_points()[-1],
                graph.get_points()[-1][0]*RIGHT + h_line.get_center()[1]*UP
            )
            brace.set_height(v_line.get_height())
            brace.next_to(v_line, RIGHT, SMALL_BUFF)
            label.set_height(min(
                label.get_height(),
                brace.get_height()
            ))
            label.next_to(brace, RIGHT, SMALL_BUFF)

        self.add(ode)
        self.play(
            Write(T_room_label),
            ShowCreation(h_line, run_time = 2)
        )
        if self.include_solution:
            self.play(Write(solution))
        graph_growth = ShowCreation(graph, rate_func=linear)
        delta_T_group_update = UpdateFromFunc(
            delta_T_group, update_delta_T_group
        )
        self.play(
            GrowFromCenter(delta_T_brace),
            Write(delta_T_label),
        )
        self.play(graph_growth, delta_T_group_update, run_time = 15)
        self.wait(2)


class TemperatureOverTimeOfWarmWaterWithSolution(TemperatureOverTimeOfWarmWater):
    CONFIG = {
        "include_solution" : True
    }
