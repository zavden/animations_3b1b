# ==============================================================================
# Scene:      GraphIntegral
# Source:     videos/_2017/eoc/old_chapter1.py (lines 2025-2189)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GraphIntegral.py GraphIntegral -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GraphIntegral(GraphScene):
    CONFIG = {
        "x_min" : -0.25,
        "x_max" : 4,
        "x_tick_frequency" : 0.25,
        "x_leftmost_tick" : -0.25,
        "x_labeled_nums" : list(range(1, 5)),
        "x_axis_label" : "r",
        "y_min" : -2,
        "y_max" : 25,
        "y_tick_frequency" : 2.5,
        "y_bottom_tick" : 0,
        "y_labeled_nums" : list(range(5, 30, 5)),
        "y_axis_label" : "",
        "dr" : 0.125,
        "R" : 3.5,
    }
    def construct(self):
        self.func = lambda r : 2*np.pi*r
        integral = OldTex("\\int_0^R 2\\pi r \\, dr")
        integral.to_edge(UP).shift(LEFT)
        self.little_r = integral[5]

        self.play(Write(integral))
        self.wait()
        self.setup_axes()
        self.show_horizontal_axis()
        self.add_rectangles()
        self.thinner_rectangles()
        self.ask_about_area()

    def show_horizontal_axis(self):
        arrows = [
            Arrow(self.little_r, self.coords_to_point(*coords))
            for coords in ((0, 0), (self.x_max, 0))
        ]
        moving_arrow = arrows[0].copy()
        self.play(
            ShowCreation(moving_arrow),
            self.little_r.set_color, YELLOW
        )
        for arrow in reversed(arrows):
            self.play(Transform(moving_arrow, arrow, run_time = 4))
        self.play(
            FadeOut(moving_arrow),
            self.little_r.set_color, WHITE
        )
        
    def add_rectangles(self):
        tick_height = 0.2
        special_tick_index = 12
        ticks = VGroup(*[
            Line(UP, DOWN).move_to(self.coords_to_point(x, 0))
            for x in np.arange(0, self.R+self.dr, self.dr)
        ])
        ticks.stretch_to_fit_height(tick_height)
        ticks.set_color(YELLOW)
        R_label = OldTex("R")
        R_label.next_to(self.coords_to_point(self.R, 0), DOWN)

        values_words = OldTexText("Values of $r$")
        values_words.shift(UP)
        arrows = VGroup(*[
            Arrow(
                values_words.get_bottom(), 
                tick.get_center(), 
                tip_length = 0.15
            )
            for tick in ticks
        ])

        dr_brace = Brace(
            VGroup(*ticks[special_tick_index:special_tick_index+2]), 
            buff = SMALL_BUFF
        )
        dr_text = dr_brace.get_text("$dr$", buff = SMALL_BUFF)
        # dr_text.set_color(YELLOW)

        rectangles = self.get_rectangles(self.dr)
        special_rect = rectangles[special_tick_index]
        left_brace = Brace(special_rect, LEFT)
        height_label = left_brace.get_text("$2\\pi r$")

        self.play(
            ShowCreation(ticks, lag_ratio = 0.5),
            Write(R_label)
        )
        self.play(
            Write(values_words),
            ShowCreation(arrows)
        )
        self.wait()
        self.play(
            GrowFromCenter(dr_brace),
            Write(dr_text)
        )
        self.wait()
        rectangles.save_state()
        rectangles.stretch_to_fit_height(0)
        rectangles.move_to(self.graph_origin, DOWN+LEFT)
        self.play(*list(map(FadeOut, [arrows, values_words])))
        self.play(
            rectangles.restore, 
            Animation(ticks),
            run_time = 2
        )
        self.wait()
        self.play(*[
            ApplyMethod(rect.fade, 0.7)
            for rect in rectangles
            if rect is not special_rect
        ] + [Animation(ticks)])
        self.play(
            GrowFromCenter(left_brace),
            Write(height_label)
        )
        self.wait()

        graph = self.graph_function(
            lambda r : 2*np.pi*r, 
            animate = False
        )
        graph_label = self.label_graph(
            self.graph, "f(r) = 2\\pi r", 
            proportion = 0.5,
            direction = LEFT,
            animate = False
        )
        self.play(
            rectangles.restore,
            Animation(ticks),
            FadeOut(left_brace),
            Transform(height_label, graph_label),
            ShowCreation(graph)
        )
        self.wait(3)
        self.play(*list(map(FadeOut, [ticks, dr_brace, dr_text])))
        self.rectangles = rectangles

    def thinner_rectangles(self):
        for x in range(2, 8):
            new_rects = self.get_rectangles(
                dr = self.dr/x, stroke_width = 1./x
            )
            self.play(Transform(self.rectangles, new_rects))
        self.wait()

    def ask_about_area(self):
        question = OldTexText("What's this \\\\ area")
        question.to_edge(RIGHT).shift(2*UP)
        arrow = Arrow(
            question.get_bottom(), 
            self.rectangles, 
            buff = SMALL_BUFF
        )
        self.play(
            Write(question),
            ShowCreation(arrow)
        )
        self.wait()

    def get_rectangles(self, dr, stroke_width = 1):
        return self.get_riemann_rectangles(
            0, self.R, dr, stroke_width = stroke_width
        )
