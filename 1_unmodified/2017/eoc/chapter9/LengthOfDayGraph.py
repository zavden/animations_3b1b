# ==============================================================================
# Scene:      LengthOfDayGraph
# Source:     videos/_2017/eoc/chapter9.py (lines 183-343)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LengthOfDayGraph.py LengthOfDayGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LengthOfDayGraph(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_max" : 365,
        "x_axis_width" : 12,
        "x_tick_frequency" : 25,
        "x_labeled_nums" : list(range(50, 365, 50)),
        "x_axis_label" : "Days since March 21",
        "y_min" : 0,
        "y_max" : 16,
        "y_axis_height" : 6,
        "y_tick_frequency" : 1,
        "y_labeled_nums" : list(range(2, 15, 2)),
        "y_axis_label" : "Hours of daylight",
        "graph_origin" : 6*LEFT + 3*DOWN,
        "camera_class" : ThreeDCamera,
        "camera_config" : {
            "shading_factor" : 1,
        }
    }
    def construct(self):
        self.setup_axes()
        self.add_graph()
        self.show_solar_pannel()
        self.set_color_summer_months()
        self.mention_constants()

    def add_graph(self):
        x_label = self.x_axis_label_mob
        y_label = self.y_axis_label_mob

        graph = self.get_graph(
            lambda x : 2.7*np.sin((2*np.pi)*x/365 ) + 12.4,
            color = GREEN,
        )
        graph_label = OldTex("2.7\\sin(2\\pi x/365) + 12.4")
        graph_label.to_corner(UP+RIGHT).shift(LEFT)
        VGroup(*graph_label[3:6]).set_color(graph.get_color())
        graph_label[9].set_color(YELLOW)

        self.remove(x_label, y_label)
        for label in y_label, x_label:
            self.play(FadeIn(
                label, 
                run_time = 2,
                lag_ratio = 0.5
            ))
        self.play(
            ShowCreation(graph, rate_func=linear),
            FadeIn(
                graph_label,
                rate_func = squish_rate_func(smooth, 0.5, 1),
                lag_ratio = 0.5
            ),
            run_time = 3,
        )
        self.wait()

        self.graph = graph 
        self.graph_label = graph_label

    def show_solar_pannel(self):
        randy = Randolph()
        randy.to_edge(DOWN)
        panel = ThreeDMobject(*[
            Rectangle(
                height = 0.7, width = 0.25,
                fill_color = GREY_D,
                fill_opacity = 1,
                stroke_width = 1,
                stroke_color = GREY,
            )
            for x in range(6)
        ])
        panel.arrange(RIGHT, buff = SMALL_BUFF)
        panel.center()
        panels = ThreeDMobject(panel, panel.copy(), panel.copy())
        panels.arrange(DOWN)
        panels.rotate(4*np.pi/12, DOWN)
        panels.rotate(-np.pi/6, OUT)
        side_vect = RIGHT
        side_vect = rotate_vector(side_vect, 4*np.pi/12, DOWN)
        side_vect = rotate_vector(side_vect, -np.pi/3, OUT)
        panels.next_to(randy.get_corner(UP+RIGHT), RIGHT)

        self.play(FadeIn(randy))
        self.play(
            randy.change, "thinking", panels.get_right(),
            FadeIn(
                panels, 
                run_time = 2,
                lag_ratio = 0.5
            )
        )
        for angle in -np.pi/4, np.pi/4:
            self.play(*[
                Rotate(
                    panel, angle,
                    axis = side_vect,
                    in_place = True,
                    run_time = 2,
                    rate_func = squish_rate_func(smooth, a, a+0.8)              
                )
                for panel, a in zip(panels, np.linspace(0, 0.2, len(panels)))
            ])
        self.play(Blink(randy))
        self.play(*list(map(FadeOut, [randy, panels])))

    def set_color_summer_months(self):
        summer_rect = Rectangle()
        summer_rect.set_stroke(width = 0)
        summer_rect.set_fill(YELLOW, opacity = 0.25)
        summer_rect.replace(Line(
            self.graph_origin,
            self.coords_to_point(365/2, 15.5)
        ), stretch = True)

        winter_rect = Rectangle()
        winter_rect.set_stroke(width = 0)
        winter_rect.set_fill(BLUE, opacity = 0.25)
        winter_rect.replace(Line(
            self.coords_to_point(365/2, 15.5),
            self.coords_to_point(365, 0),
        ), stretch = True)


        summer_words, winter_words = [
            OldTexText("%s \\\\ months"%s).move_to(rect)
            for s, rect in [
                ("Summer", summer_rect),
                ("Winter", winter_rect),
            ]
        ]

        for rect, words in (summer_rect, summer_words), (winter_rect, winter_words):
            self.play(
                FadeIn(rect),
                Write(words, run_time = 2)
            )
        self.wait()

    def mention_constants(self):
        #2.7\\sin(2\\pi t/365) + 12.4
        constants = VGroup(*[
            VGroup(*self.graph_label[i:j])
            for i, j in [(0, 3), (7, 9), (11, 14), (16, 20)]
        ])

        self.play(*[
            ApplyFunction(
                lambda c : c.scale(0.9).shift(SMALL_BUFF*DOWN).set_color(RED),
                constant,
                run_time = 3,
                rate_func = squish_rate_func(there_and_back, a, a+0.7)
            )
            for constant, a in zip(
                constants, 
                np.linspace(0, 0.3, len(constants))
            )
        ])
        self.wait()
