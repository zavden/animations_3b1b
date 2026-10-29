# ==============================================================================
# Scene:      NegativeArea
# Source:     videos/_2017/eoc/chapter8.py (lines 2475-2681)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl NegativeArea.py NegativeArea -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

DISTANCE_COLOR = BLUE


TIME_COLOR = YELLOW


VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter8.py -----

class NegativeArea(GraphScene):
    CONFIG = {
        "x_axis_label" : "Time",
        "y_axis_label" : "Velocity",
        "graph_origin" : 1.5*DOWN + 5*LEFT,
        "y_min" : -3,
        "y_max" : 7,
        "small_dx" : 0.01,
        "sample_input" : 5,
    }
    def construct(self):
        self.setup_axes()
        self.add_graph_and_area()
        self.write_negative_area()
        self.show_negative_point()
        self.show_car_going_backwards()
        self.write_v_dt()
        self.show_rectangle()
        self.write_signed_area()

    def add_graph_and_area(self):
        graph = self.get_graph(
            lambda x : -0.02*(x+1)*(x-3)*(x-7)*(x-10),
            x_min = 0,
            x_max = 8,
            color = VELOCITY_COLOR
        )
        area = self.get_riemann_rectangles(
            graph, 
            x_min = 0,
            x_max = 8,
            dx = self.small_dx,
            start_color = BLUE_D,
            end_color = BLUE_D,
            fill_opacity = 0.75,
            stroke_width = 0,
        )

        self .play(
            ShowCreation(graph),
            FadeIn(
                area, 
                run_time = 2,
                lag_ratio = 0.5,
            )
        )

        self.graph = graph
        self.area = area

    def write_negative_area(self):
        words = OldTexText("Negative area")
        words.set_color(RED)
        words.next_to(
            self.coords_to_point(7, -2),
            RIGHT,
        )
        arrow = Arrow(words, self.coords_to_point(
            self.sample_input, -1,
        ))

        self.play(
            Write(words, run_time = 2),
            ShowCreation(arrow)
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [self.area, arrow])))

        self.negative_area_words = words

    def show_negative_point(self):
        v_line = self.get_vertical_line_to_graph(
            self.sample_input, self.graph,
            color = RED
        )
        self.play(ShowCreation(v_line))
        self.wait()
        self.v_line = v_line

    def show_car_going_backwards(self):
        car = Car()
        start_point = 3*RIGHT + 2*UP
        end_point = start_point + LEFT
        nudged_end_point = end_point + MED_SMALL_BUFF*LEFT
        car.move_to(start_point)
        arrow = Arrow(RIGHT, LEFT, color = RED)
        arrow.next_to(car, UP+LEFT)
        arrow.shift(MED_LARGE_BUFF*RIGHT)

        self.play(FadeIn(car))
        self.play(ShowCreation(arrow))
        self.play(MoveCar(
            car, end_point, 
            moving_forward = False,
            run_time = 3
        ))
        self.wait()
        ghost_car = car.copy().fade()
        right_nose_line = self.get_car_nose_line(car)
        self.play(ShowCreation(right_nose_line))
        self.add(ghost_car)
        self.play(MoveCar(
            car, nudged_end_point,
            moving_forward = False
        ))
        left_nose_line = self.get_car_nose_line(car)
        self.play(ShowCreation(left_nose_line))

        self.nose_lines = VGroup(left_nose_line, right_nose_line)
        self.car = car
        self.ghost_car = ghost_car

    def write_v_dt(self):
        brace = Brace(self.nose_lines, DOWN, buff = 0)
        equation = OldTex("ds", "=", "v(t)", "dt")
        equation.next_to(brace, DOWN, SMALL_BUFF, LEFT)
        equation.set_color_by_tex("ds", DISTANCE_COLOR)
        equation.set_color_by_tex("dt", TIME_COLOR)

        negative = OldTexText("Negative")
        negative.set_color(RED)
        negative.next_to(equation.get_corner(UP+RIGHT), UP, LARGE_BUFF)
        ds_arrow, v_arrow = arrows = VGroup(*[
            Arrow(
                negative.get_bottom(),
                equation.get_part_by_tex(tex).get_top(),
                color = RED,
            )
            for tex in ("ds", "v(t)")
        ])

        self.play(
            GrowFromCenter(brace),
            Write(equation)
        )
        self.wait()
        self.play(FadeIn(negative))
        self.play(ShowCreation(v_arrow))
        self.wait(2)
        self.play(ReplacementTransform(
            v_arrow.copy(),
            ds_arrow
        ))
        self.wait(2)

        self.ds_equation = equation
        self.negative_word = negative
        self.negative_word_arrows = arrows

    def show_rectangle(self):
        rect_list = self.get_riemann_rectangles_list(
            self.graph, x_min = 0, x_max = 8,
            n_iterations = 6,
            start_color = BLUE_D,
            end_color = BLUE_D,
            fill_opacity = 0.75,
        )
        rects = rect_list[0]
        rect = rects[len(rects)*self.sample_input//8]

        dt_brace = Brace(rect, UP, buff = 0)
        v_brace = Brace(rect, LEFT, buff = 0)
        dt_label = dt_brace.get_text("$dt$", buff = SMALL_BUFF)
        dt_label.set_color(YELLOW)
        v_label = v_brace.get_text("$v(t)$", buff = SMALL_BUFF)
        v_label.add_background_rectangle()

        self.play(FadeOut(self.v_line), FadeIn(rect))
        self.play(
            GrowFromCenter(dt_brace), 
            GrowFromCenter(v_brace), 
            Write(dt_label),
            Write(v_label),
        )
        self.wait(2)
        self.play(*it.chain(
            [FadeIn(r) for r in rects if r is not rect],
            list(map(FadeOut, [
                dt_brace, v_brace, dt_label, v_label
            ]))
        ))
        self.wait()
        for new_rects in rect_list[1:]:
            self.transform_between_riemann_rects(rects, new_rects)
        self.wait()

    def write_signed_area(self):
        words = OldTexText("``Signed area''")
        words.next_to(self.coords_to_point(self.sample_input, 0), UP)
        symbols = VGroup(*[
            OldTex(sym).move_to(self.coords_to_point(*coords))
            for sym, coords in [
                ("+", (1, 2)),
                ("-", (5, -1)),
                ("+", (7.6, 0.5)),
            ]
        ])
        self.play(Write(words))
        self.play(Write(symbols))
        self.wait()

    ####

    def get_car_nose_line(self, car):
        line = DashedLine(car.get_top(), car.get_bottom())
        line.move_to(car.get_right())
        return line
