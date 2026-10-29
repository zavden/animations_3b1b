# ==============================================================================
# Scene:      PeopleValueGraph
# Source:     videos/_2018/div_curl.py (lines 4416-4512)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PeopleValueGraph.py PeopleValueGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PeopleValueGraph(GraphScene):
    CONFIG = {
        "x_axis_label": "People reached",
        "y_axis_label": "Value per person",
        "x_min": 0,
        "x_max": 12,
        "x_axis_width": 11,
        "y_max": 8,
        "y_axis_height": 5,
        "graph_origin": 2 * DOWN + 5 * LEFT,
        "riemann_rectangles_config": {
            "dx": 0.01,
            "stroke_width": 0,
            "start_color": GREEN,
            "end_color": BLUE,
        }
    }

    def construct(self):
        self.setup_axes()
        self.tweak_labels()
        self.add_curve()
        self.comment_on_incentives()
        self.change_curve()

    def tweak_labels(self):
        self.add_foreground_mobjects(self.x_axis_label_mob)
        self.y_axis_label_mob.to_edge(LEFT)

    def add_curve(self):
        graph = self.graph = self.get_graph(
            lambda x: 7 * np.exp(-0.5 * x),
        )

        self.play(
            ShowCreation(graph),
            rate_func=bezier([0, 0, 1, 1]),
            run_time=3
        )

    def comment_on_incentives(self):
        reach_arrow = Vector(5 * RIGHT)
        reach_arrow.next_to(
            self.x_axis, DOWN,
            buff=SMALL_BUFF,
            aligned_edge=RIGHT
        )
        reach_words = OldTexText("Maximize reach?")
        reach_words.next_to(reach_arrow, DOWN, buff=SMALL_BUFF)
        reach_words.match_color(reach_arrow)

        area = self.area = self.get_riemann_rectangles(
            self.graph, **self.riemann_rectangles_config
        )
        area_words = OldTexText("Maximize this area")
        area_words.set_color(BLUE)
        area_words.move_to(self.coords_to_point(4, 5))
        area_arrow = Arrow(
            area_words.get_bottom(),
            self.coords_to_point(1.5, 2)
        )

        self.play(GrowArrow(reach_arrow))
        self.play(Write(reach_words))
        self.wait()
        self.play(
            LaggedStartMap(DrawBorderThenFill, area),
            Animation(self.graph),
            Animation(self.axes),
            Write(area_words),
            GrowArrow(area_arrow),
        )
        self.wait()

        self.area_label_group = VGroup(area_words, area_arrow)

    def change_curve(self):
        new_graph = self.get_graph(
            lambda x: interpolate(
                7 * np.exp(-0.01 * x),
                7 * np.exp(-3 * x),
                smooth(np.clip(x / 5, 0, 1))
            )
        )
        new_area = self.get_riemann_rectangles(
            new_graph, **self.riemann_rectangles_config
        )

        self.play(
            Transform(self.area, new_area),
            Transform(self.graph, new_graph),
            self.area_label_group[0].shift, RIGHT,
            Animation(self.area_label_group),
            Animation(self.axes),
            run_time=4,
        )
        self.wait()
