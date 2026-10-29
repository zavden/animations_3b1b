# ==============================================================================
# Scene:      RepeatedApplicationGraphically
# Source:     videos/_2018/alt_calc.py (lines 2819-2896)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RepeatedApplicationGraphically.py RepeatedApplicationGraphically -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class GraphOnePlusOneOverX(GraphScene):
    CONFIG = {
        "x_min": -6,
        "x_max": 6,
        "x_axis_width": 12,
        "y_min": -4,
        "y_max": 5,
        "y_axis_height": 8,
        "y_axis_label": None,
        "graph_origin": 0.5 * DOWN,
        "num_graph_anchor_points": 100,
        "func_graph_color": GREEN,
        "identity_graph_color": BLUE,
    }

    def construct(self):
        self.add_title()
        self.setup_axes()
        self.draw_graphs()
        self.show_solutions()

    def add_title(self):
        title = self.title = OldTex(
            "\\text{Solve: }", "1 + \\frac{1}{x}", "=", "x",
        )
        title.set_color_by_tex("x", self.identity_graph_color, substring=False)
        title.set_color_by_tex("frac", self.func_graph_color)
        title.to_corner(UL)
        self.add(title)

    def setup_axes(self):
        GraphScene.setup_axes(self)
        step = 2
        self.x_axis.add_numbers(*list(range(-6, 0, step)) + list(range(step, 7, step)))
        self.y_axis.label_direction = RIGHT
        self.y_axis.add_numbers(*list(range(-2, 0, step)) + list(range(step, 4, step)))

    def draw_graphs(self, animate=True):
        lower_func_graph, upper_func_graph = func_graph = VGroup(*[
            self.get_graph(
                lambda x: 1.0 + 1.0 / x,
                x_min=x_min,
                x_max=x_max,
                color=self.func_graph_color,
            )
            for x_min, x_max in [(-10, -0.1), (0.1, 10)]
        ])
        func_graph.label = self.get_graph_label(
            upper_func_graph, "y = 1 + \\frac{1}{x}",
            x_val=6, direction=UP,
        )

        identity_graph = self.get_graph(
            lambda x: x, color=self.identity_graph_color
        )
        identity_graph.label = self.get_graph_label(
            identity_graph, "y = x",
            x_val=3, direction=UL, buff=SMALL_BUFF
        )

        if animate:
            for graph in func_graph, identity_graph:
                self.play(
                    ShowCreation(graph),
                    Write(graph.label),
                    run_time=2
                )
            self.wait()
        else:
            self.add(
                func_graph, func_graph.label,
                identity_graph, identity_graph.label,
            )

        self.func_graph = func_graph
        self.identity_graph = identity_graph

    def show_solutions(self):
        phi = 0.5 * (1 + np.sqrt(5))
        phi_bro = 0.5 * (1 - np.sqrt(5))

        lines = VGroup()
        for num in phi, phi_bro:
            line = DashedLine(
                self.coords_to_point(num, 0),
                self.coords_to_point(num, num),
                color=WHITE
            )
            line_copy = line.copy()
            line_copy.set_color(YELLOW)
            line.fade(0.5)
            line_anim = ShowCreationThenDestruction(
                line_copy,
                lag_ratio=0.5,
                run_time=2
            )
            cycle_animation(line_anim)
            lines.add(line)

        phi_line, phi_bro_line = lines

        decimal_kwargs = {
            "num_decimal_places": 3,
            "show_ellipsis": True,
            "color": YELLOW,
        }
        arrow_kwargs = {
            "buff": SMALL_BUFF,
            "color": WHITE,
            "tip_length": 0.15,
            "rectangular_stem_width": 0.025,
        }

        phi_decimal = DecimalNumber(phi, **decimal_kwargs)
        phi_decimal.next_to(phi_line, DOWN, LARGE_BUFF)
        phi_arrow = Arrow(
            phi_decimal[:4].get_top(), phi_line.get_bottom(),
            **arrow_kwargs
        )
        phi_label = OldTex("=", "\\varphi")
        phi_label.next_to(phi_decimal, RIGHT)
        phi_label.set_color_by_tex("\\varphi", YELLOW)

        phi_bro_decimal = DecimalNumber(phi_bro, **decimal_kwargs)
        phi_bro_decimal.next_to(phi_bro_line, UP, LARGE_BUFF)
        phi_bro_decimal.shift(0.5 * LEFT)
        phi_bro_arrow = Arrow(
            phi_bro_decimal[:6].get_bottom(), phi_bro_line.get_top(),
            **arrow_kwargs
        )

        brother_words = OldTexText(
            "$\\varphi$'s little brother",
            tex_to_color_map={"$\\varphi$": YELLOW},
            arg_separator=""
        )
        brother_words.next_to(
            phi_bro_decimal[-2], UP, buff=MED_SMALL_BUFF,
            aligned_edge=RIGHT
        )

        self.add(phi_line.continual_anim)
        self.play(ShowCreation(phi_line))
        self.play(
            Write(phi_decimal),
            GrowArrow(phi_arrow),
        )
        self.play(Write(phi_label))
        self.wait(3)
        self.add(phi_bro_line.continual_anim)
        self.play(ShowCreation(phi_bro_line))
        self.play(
            Write(phi_bro_decimal),
            GrowArrow(phi_bro_arrow),
        )
        self.wait(4)
        self.play(Write(brother_words))
        self.wait(8)


class RepeatedApplicationGraphically(GraphOnePlusOneOverX, PiCreatureScene):
    CONFIG = {
        "starting_value": 1,
        "n_jumps": 5,
        "n_times_to_show_identity_property": 2,
    }

    def setup(self):
        GraphOnePlusOneOverX.setup(self)
        PiCreatureScene.setup(self)

    def construct(self):
        self.setup_axes()
        self.draw_graphs(animate=False)
        self.draw_spider_web()

    def create_pi_creature(self):
        randy = Randolph(height=2)
        randy.flip()
        randy.to_corner(DR)
        return randy

    def get_new_randy_mode(self):
        randy = self.pi_creature
        if not hasattr(self, "n_mode_changes"):
            self.n_mode_changes = 0
        else:
            self.n_mode_changes += 1
        if self.n_mode_changes % 3 != 0:
            return randy.get_mode()
        return random.choice([
            "confused",
            "erm",
            "maybe"
        ])

    def draw_spider_web(self):
        randy = self.pi_creature
        func = self.func_graph[0].underlying_function
        x_val = self.starting_value
        curr_output = 0
        dot = Dot(color=RED, fill_opacity=0.7)
        dot.move_to(self.coords_to_point(x_val, curr_output))

        self.play(FadeIn(dot, 2 * UR))
        self.wait()

        for n in range(self.n_jumps):
            new_output = func(x_val)
            func_graph_point = self.coords_to_point(x_val, new_output)
            id_graph_point = self.coords_to_point(new_output, new_output)
            v_line = DashedLine(dot.get_center(), func_graph_point)
            h_line = DashedLine(func_graph_point, id_graph_point)

            curr_output = new_output
            x_val = new_output

            for line in v_line, h_line:
                line_end = line.get_end()
                self.play(
                    ShowCreation(line),
                    dot.move_to, line_end,
                    randy.change, self.get_new_randy_mode()
                )
                self.wait()

            if n < self.n_times_to_show_identity_property:
                x_point = self.coords_to_point(new_output, 0)
                y_point = self.coords_to_point(0, new_output)
                lines = VGroup(*[
                    Line(dot.get_center(), point)
                    for point in (x_point, y_point)
                ])
                lines.set_color(YELLOW)
                self.play(ShowCreationThenDestruction(
                    lines, run_time=2
                ))
                self.wait(0.25)
