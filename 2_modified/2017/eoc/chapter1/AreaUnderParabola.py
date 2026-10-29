# ==============================================================================
# Scene:      AreaUnderParabola
# Source:     videos/_2017/eoc/chapter1.py (lines 2010-2209)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AreaUnderParabola.py AreaUnderParabola -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 integer division used as list index
# ==============================================================================

from manim_imports_ext import *

class AreaUnderParabola(GraphScene):
    CONFIG = {
        "x_max" : 4,
        "x_labeled_nums" : list(range(-1, 5)),
        "y_min" : 0,
        "y_max" : 15,
        "y_tick_frequency" : 2.5,
        "y_labeled_nums" : list(range(5, 20, 5)),
        "n_rect_iterations" : 6,
        "default_right_x" : 3,
        "func" : lambda x : x**2,
        "graph_label_tex" : "x^2",
        "graph_label_x_val" : 3.8,
    }
    def construct(self):
        self.setup_axes()
        self.show_graph()
        self.show_area()
        self.ask_about_area()
        self.show_confusion()
        self.show_variable_endpoint()
        self.name_integral()

    def show_graph(self):
        graph = self.get_graph(self.func)
        graph_label = self.get_graph_label(
            graph, self.graph_label_tex, 
            direction = LEFT,
            x_val = self.graph_label_x_val,
        )

        self.play(ShowCreation(graph))
        self.play(Write(graph_label))
        self.wait()

        self.graph = graph
        self.graph_label = graph_label

    def show_area(self):
        dx_list = [0.25/(2**n) for n in range(self.n_rect_iterations)]
        rect_lists = [
            self.get_riemann_rectangles(
                self.graph,
                x_min = 0,
                x_max = self.default_right_x,
                dx = dx,
                stroke_width = 4*dx,
            )
            for dx in dx_list
        ]
        rects = rect_lists[0]
        foreground_mobjects = [self.axes, self.graph]

        self.play(
            DrawBorderThenFill(
                rects,
                run_time = 2,
                rate_func = smooth,
                lag_ratio = 0.5,
            ),
            *list(map(Animation, foreground_mobjects))
        )
        self.wait()
        for new_rects in rect_lists[1:]:
            self.play(
                Transform(
                    rects, new_rects,
                    lag_ratio = 0.5,
                ), 
                *list(map(Animation, foreground_mobjects))
            )
        self.wait()

        self.rects = rects
        self.dx = dx_list[-1]
        self.foreground_mobjects = foreground_mobjects

    def ask_about_area(self):
        rects = self.rects
        question = OldTexText("Area?")
        question.move_to(rects.get_top(), DOWN)
        # CHANGE: Python 2 integer division used as list index
        mid_rect = rects[2*len(rects)//3]
        arrow = Arrow(question.get_bottom(), mid_rect.get_center())

        v_lines = VGroup(*[
            DashedLine(
                FRAME_HEIGHT*UP, ORIGIN,
                color = RED
            ).move_to(self.coords_to_point(x, 0), DOWN)
            for x in (0, self.default_right_x)
        ])

        self.play(
            Write(question),
            ShowCreation(arrow)
        )
        self.wait()
        self.play(ShowCreation(v_lines, run_time = 2))
        self.wait()

        self.foreground_mobjects += [question, arrow]
        self.question = question
        self.question_arrow = arrow
        self.v_lines = v_lines

    def show_confusion(self):
        morty = Mortimer()
        morty.to_corner(DOWN+RIGHT)

        self.play(FadeIn(morty))
        self.play(
            morty.change_mode, "confused",
            morty.look_at, self.question,
        )
        self.play(morty.look_at, self.rects.get_bottom())
        self.play(Blink(morty))
        self.play(morty.look_at, self.question)
        self.wait()
        self.play(Blink(morty))
        self.play(FadeOut(morty))

    def show_variable_endpoint(self):
        triangle = RegularPolygon(
            n = 3,
            start_angle = np.pi/2,
            stroke_width = 0,
            fill_color = WHITE,
            fill_opacity = 1,
        )
        triangle.set_height(0.25)
        triangle.move_to(self.v_lines[1].get_bottom(), UP)
        x_label = OldTex("x")
        x_label.next_to(triangle, DOWN)
        self.right_point_slider = VGroup(triangle, x_label)

        A_func = OldTex("A(x)")
        A_func.move_to(self.question, DOWN)

        self.play(FadeOut(self.x_axis.numbers))
        self.x_axis.remove(*self.x_axis.numbers)
        self.foreground_mobjects.remove(self.axes)
        self.play(DrawBorderThenFill(self.right_point_slider))
        self.move_right_point_to(2)
        self.wait()
        self.move_right_point_to(self.default_right_x)
        self.wait()
        self.play(ReplacementTransform(self.question, A_func))
        self.wait()

        self.A_func = A_func

    def name_integral(self):
        f_tex = "$%s$"%self.graph_label_tex
        words = OldTexText("``Integral'' of ", f_tex)
        words.set_color_by_tex(f_tex, self.graph_label.get_color())
        brace = Brace(self.A_func, UP)
        words.next_to(brace, UP)

        self.play(
            Write(words),
            GrowFromCenter(brace)
        )
        self.wait()
        for x in 4, 2, self.default_right_x:
            self.move_right_point_to(x, run_time = 2)

        self.integral_words_group = VGroup(brace, words)

    ####

    def move_right_point_to(self, target_x, **kwargs):
        v_line = self.v_lines[1]
        slider = self.right_point_slider
        rects = self.rects
        curr_x = self.x_axis.point_to_number(v_line.get_bottom())

        group = VGroup(rects, v_line, slider)
        def update_group(group, alpha):
            rects, v_line, slider = group
            new_x = interpolate(curr_x, target_x, alpha)
            new_rects = self.get_riemann_rectangles(
                self.graph,
                x_min = 0,
                x_max = new_x,
                dx = self.dx*new_x/3.0,
                stroke_width = rects[0].get_stroke_width(),
            )
            point = self.coords_to_point(new_x, 0)
            v_line.move_to(point, DOWN)
            slider.move_to(point, UP)
            Transform(rects, new_rects).update(1)
            return VGroup(rects, v_line, slider)

        self.play(
            UpdateFromAlphaFunc(
                group, update_group,
                **kwargs
            ),
            *list(map(Animation, self.foreground_mobjects))
        )
