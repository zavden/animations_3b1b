# ==============================================================================
# Scene:      NumericalPlayOnNumberLineFromOne
# Source:     videos/_2018/alt_calc.py (lines 2685-2777)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NumericalPlayOnNumberLineFromOne.py NumericalPlayOnNumberLineFromOne -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class NumericalPlayOnNumberLineFromOne(Scene):
    CONFIG = {
        "starting_value": 1,
        "n_jumps": 10,
        "func": lambda x: 1 + 1.0 / x,
        "number_line_config": {
            "x_min": 0,
            "x_max": 2,
            "unit_size": 6,
            "tick_frequency": 0.25,
            "big_tick_numbers": [0, 1, 2]
        }
    }

    def construct(self):
        self.add_number_line()
        self.add_phi_label()
        self.add_title()
        self.bounce_around()

    def add_number_line(self):
        number_line = NumberLine(**self.number_line_config)
        number_line.move_to(2 * DOWN)
        number_line.add_numbers()

        self.add(number_line)
        self.number_line = number_line

    def add_phi_label(self):
        number_line = self.number_line
        phi_point = number_line.number_to_point(
            (1 + np.sqrt(5)) / 2
        )
        phi_dot = Dot(phi_point, color=YELLOW)
        arrow = Vector(DL)
        arrow.next_to(phi_point, UR, SMALL_BUFF)
        phi_label = OldTex("\\varphi = 1.618\\dots")
        phi_label.set_color(YELLOW)
        phi_label.next_to(arrow.get_start(), UP, SMALL_BUFF)

        self.add(phi_dot, phi_label, arrow)

    def add_title(self):
        title = OldTex("x \\rightarrow 1 + \\frac{1}{x}")
        title.to_corner(UL)
        self.add(title)

    def bounce_around(self):
        number_line = self.number_line
        value = self.starting_value
        point = number_line.number_to_point(value)
        dot = Dot(point)
        dot.set_fill(RED, opacity=0.8)
        arrow = Vector(DR)
        arrow.next_to(point, UL, buff=SMALL_BUFF)
        arrow.match_color(dot)
        start_here = OldTexText("Start here")
        start_here.next_to(arrow.get_start(), UP, SMALL_BUFF)
        start_here.match_color(dot)

        self.play(
            FadeIn(start_here),
            GrowArrow(arrow),
            GrowFromPoint(dot, arrow.get_start())
        )
        self.play(
            FadeOut(start_here),
            FadeOut(arrow)
        )
        self.wait()
        for x in range(self.n_jumps):
            new_value = self.func(value)
            new_point = number_line.number_to_point(new_value)
            if new_value - value > 0:
                path_arc = -120 * DEGREES
            else:
                path_arc = -120 * DEGREES
            arc = Line(
                point, new_point,
                path_arc=path_arc,
                buff=SMALL_BUFF
            )
            self.play(
                ShowCreationThenDestruction(arc, run_time=1.5),
                ApplyMethod(
                    dot.move_to, new_point,
                    path_arc=path_arc
                ),
            )
            self.wait(0.5)

            value = new_value
            point = new_point
