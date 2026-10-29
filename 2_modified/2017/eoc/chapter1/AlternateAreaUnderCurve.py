# ==============================================================================
# Scene:      AlternateAreaUnderCurve
# Source:     videos/_2017/eoc/chapter1.py (lines 2545-2643)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AlternateAreaUnderCurve.py AlternateAreaUnderCurve -w -m --fps 15
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


class PlayingTowardsDADX(AreaUnderParabola, ReconfigurableScene):
    CONFIG = {
        "n_rect_iterations" : 6,
        "deriv_dx" : 0.2,
        "graph_origin" : 2.5*DOWN + 6*LEFT,
    }
    def setup(self):
        AreaUnderParabola.setup(self)
        ReconfigurableScene.setup(self)

    def construct(self):
        self.fast_forward_to_end_of_previous_scene()

        self.nudge_x()
        self.describe_sliver()
        self.shrink_dx()
        self.write_dA_dx()
        self.dA_remains_a_mystery()
        self.write_example_inputs()
        self.show_dA_dx_in_detail()
        self.show_smaller_x()

    def fast_forward_to_end_of_previous_scene(self):
        self.force_skipping()
        AreaUnderParabola.construct(self)
        self.revert_to_original_skipping_status()

    def nudge_x(self):
        shadow_rects = self.rects.copy()
        shadow_rects.set_fill(BLACK, opacity = 0.5)

        original_v_line = self.v_lines[1].copy()
        right_v_lines = VGroup(original_v_line, self.v_lines[1])
        curr_x = self.x_axis.point_to_number(original_v_line.get_bottom())

        self.add(original_v_line)
        self.foreground_mobjects.append(original_v_line)
        self.move_right_point_to(curr_x + self.deriv_dx)
        self.play(
            FadeIn(shadow_rects), 
            *list(map(Animation, self.foreground_mobjects))
        )

        self.shadow_rects = shadow_rects
        self.right_v_lines = right_v_lines

    def describe_sliver(self):
        dx_brace = Brace(self.right_v_lines, DOWN, buff = 0)
        dx_label = dx_brace.get_text("$dx$")
        dx_group = VGroup(dx_brace, dx_label)

        dA_rect = Rectangle(
            width = self.right_v_lines.get_width(),
            height = self.shadow_rects[-1].get_height(),
            stroke_width = 0,
            fill_color = YELLOW,
            fill_opacity = 0.5,
        ).move_to(self.right_v_lines, DOWN)
        dA_label = OldTex("d", "A")
        dA_label.next_to(dA_rect, RIGHT, MED_LARGE_BUFF, UP)
        dA_label.set_color(GREEN)
        dA_arrow = Arrow(
            dA_label.get_bottom()+MED_SMALL_BUFF*DOWN, 
            dA_rect.get_center(),
            buff = 0,
            color = WHITE
        )

        difference_in_area = OldTexText(
            "d", "ifference in ", "A", "rea",
            arg_separator = ""
        )
        difference_in_area.set_color_by_tex("d", GREEN)
        difference_in_area.set_color_by_tex("A", GREEN)
        difference_in_area.scale(0.7)
        difference_in_area.next_to(dA_label, UP, MED_SMALL_BUFF, LEFT)

        side_brace = Brace(dA_rect, LEFT, buff = 0)
        graph_label_copy = self.graph_label.copy()

        self.play(
            FadeOut(self.right_point_slider),
            FadeIn(dx_group)
        )
        self.play(Indicate(dx_label))
        self.wait()
        self.play(ShowCreation(dA_arrow))
        self.wait()
        self.play(Write(dA_label, run_time = 2))
        self.wait()
        self.play(
            ReplacementTransform(dA_label[0].copy(), difference_in_area[0]),
            ReplacementTransform(dA_label[1].copy(), difference_in_area[2]),
            *list(map(FadeIn, [difference_in_area[1], difference_in_area[3]]))
        )
        self.wait(2)
        self.play(FadeIn(dA_rect), Animation(dA_arrow))
        self.play(GrowFromCenter(side_brace))
        self.play(
            graph_label_copy.set_color, WHITE,
            graph_label_copy.next_to, side_brace, LEFT, SMALL_BUFF
        )
        self.wait()
        self.play(Indicate(dx_group))
        self.wait()
        self.play(FadeOut(difference_in_area))

        self.dx_group = dx_group
        self.dA_rect = dA_rect
        self.dA_label = dA_label
        self.graph_label_copy = graph_label_copy

    def shrink_dx(self, **kwargs):
        self.transition_to_alt_config(
            deriv_dx = 0.05,
            transformation_kwargs = {"run_time" : 2},
            **kwargs
        )

    def write_dA_dx(self):
        f_tex = self.graph_label_tex
        equation = OldTex("dA", "\\approx", f_tex, "dx")
        equation.to_edge(RIGHT).shift(3*UP)
        deriv_equation = OldTex(
            "{dA", "\\over \\,", "dx}", "\\approx", f_tex
        )
        deriv_equation.move_to(equation, UP+LEFT)

        for tex_mob in equation, deriv_equation:
            tex_mob.set_color_by_tex(
                "dA", self.dA_label.get_color()
            )

        dA = VGroup(self.dA_label[0][0], self.dA_label[1][0])
        x_squared = self.graph_label_copy
        dx = self.dx_group[1]

        self.play(*[
            ReplacementTransform(
                mob.copy(),
                equation.get_part_by_tex(tex),
                run_time = 2
            )
            for mob, tex in [(x_squared, f_tex), (dx, "dx"), (dA, "dA")]
        ])
        self.play(Write(equation.get_part_by_tex("approx")))
        self.wait()
        for tex, mob in (f_tex, x_squared), ("dx", dx):
            self.play(*list(map(Indicate, [
                equation.get_part_by_tex(tex),
                mob
            ])))
            self.wait(2)
        self.play(*[
            ReplacementTransform(
                equation.get_part_by_tex(tex),
                deriv_equation.get_part_by_tex(tex),
                run_time = 2,
            )
            for tex in ("dA", "approx", f_tex, "dx")
        ] + [
            Write(deriv_equation.get_part_by_tex("over"))
        ])
        self.wait(2)
        self.shrink_dx(return_to_original_configuration = False)
        self.wait()

        self.deriv_equation = deriv_equation

    def dA_remains_a_mystery(self):
        randy = Randolph(color = BLUE_C)
        randy.to_corner(DOWN+LEFT)
        randy.look_at(self.A_func)

        A_circle, dA_circle = [
            Circle(color = color).replace(
                mob, stretch = True
            ).scale(1.5)
            for mob, color in [(self.A_func, RED), (self.deriv_equation, GREEN)]
        ]
        q_marks = OldTex("???")
        q_marks.next_to(A_circle, UP)

        self.play(
            FadeOut(self.integral_words_group),
            FadeIn(randy)
        )
        self.play(
            ShowCreation(A_circle),
            randy.change_mode, "confused"
        )
        self.play(Write(q_marks, run_time = 2))
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.change_mode, "surprised",
            randy.look_at, dA_circle,
            ReplacementTransform(A_circle, dA_circle)
        )
        self.play(Blink(randy))
        self.wait()
        self.play(*list(map(FadeOut, [randy, q_marks, dA_circle])))

    def write_example_inputs(self):
        d = self.default_right_x
        three = OldTex("x =", "%d"%d)
        three_plus_dx = OldTex("x = ", "%d.001"%d)
        labels_lines_vects = list(zip(
            [three, three_plus_dx],
            self.right_v_lines,
            [LEFT, RIGHT]
        ))

        for label, line, vect in labels_lines_vects:
            point = line.get_bottom()
            label.next_to(point, DOWN+vect, MED_SMALL_BUFF)
            label.shift(LARGE_BUFF*vect)
            label.arrow = Arrow(
                label, point,
                buff = SMALL_BUFF,
                color = WHITE,
                tip_length = 0.15
            )
            line_copy = line.copy()
            line_copy.set_color(YELLOW)

            self.play(
                FadeIn(label),
                FadeIn(label.arrow),
                ShowCreation(line_copy)
            )
            self.play(FadeOut(line_copy))
        self.wait()

        self.three = three 
        self.three_plus_dx = three_plus_dx

    def show_dA_dx_in_detail(self):
        d = self.default_right_x
        expression = OldTex(
            "{A(", "%d.001"%d, ") ", "-A(", "%d"%d, ")", 
            "\\over \\,", "0.001}", 
            "\\approx", "%d"%d, "^2"
        )
        expression.scale(0.9)
        expression.next_to(
            self.deriv_equation, DOWN, MED_LARGE_BUFF
        )
        expression.to_edge(RIGHT)

        self.play(
            ReplacementTransform(
                self.three_plus_dx.get_part_by_tex("%d.001"%d).copy(),
                expression.get_part_by_tex("%d.001"%d)
            ),
            Write(VGroup(
                expression.get_part_by_tex("A("),
                expression.get_part_by_tex(")"),
            )),
        )
        self.wait()
        self.play(
            ReplacementTransform(
                self.three.get_part_by_tex("%d"%d).copy(),
                expression.get_part_by_tex("%d"%d, substring = False)
            ),
            Write(VGroup(
                expression.get_part_by_tex("-A("),
                expression.get_parts_by_tex(")")[1],
            )),
        )
        self.wait(2)
        self.play(
            Write(expression.get_part_by_tex("over")),
            ReplacementTransform(
                expression.get_part_by_tex("%d.001"%d).copy(),
                expression.get_part_by_tex("0.001"),
            )
            
        )
        self.wait()
        self.play(
            Write(expression.get_part_by_tex("approx")),
            ReplacementTransform(
                self.graph_label_copy.copy(),
                VGroup(*expression[-2:]),
                run_time = 2
            )
        )
        self.wait()

    def show_smaller_x(self):
        self.transition_to_alt_config(
            default_right_x = 2,
            deriv_dx = 0.04,
            transformation_kwargs = {"run_time" : 2}
        )


class AlternateAreaUnderCurve(PlayingTowardsDADX):
    CONFIG = {
        "func" : lambda x : (x-2)**3 - 3*(x-2) + 6,
        "graph_label_tex" : "f(x)",
        "deriv_dx" : 0.1,
        "x_max" : 5,
        "x_axis_width" : 11,
        "graph_label_x_val" : 4.5,
    }
    def construct(self):
        #Superclass parts to skip
        self.force_skipping()
        self.setup_axes()
        self.show_graph()
        self.show_area()
        self.ask_about_area()
        self.show_confusion()

        #Superclass parts to show
        self.revert_to_original_skipping_status()
        self.show_variable_endpoint()
        self.name_integral()
        self.nudge_x()
        self.describe_sliver()
        self.write_dA_dx()

        #New animations
        self.approximation_improves_for_smaller_dx()
        self.name_derivative()

    def approximation_improves_for_smaller_dx(self):
        color = YELLOW
        approx = self.deriv_equation.get_part_by_tex("approx")
        dx_to_zero_words = OldTexText(
            "Gets better \\\\ as", 
            "$dx \\to 0$"
        )
        dx_to_zero_words.set_color_by_tex("dx", color)
        dx_to_zero_words.next_to(approx, DOWN, 1.5*LARGE_BUFF)
        arrow = Arrow(dx_to_zero_words, approx, color = color)

        self.play(
            approx.set_color, color,
            ShowCreation(arrow),
            FadeIn(dx_to_zero_words),
        )
        self.wait()
        self.transition_to_alt_config(
            deriv_dx = self.deriv_dx/4.0,
            transformation_kwargs = {"run_time" : 2}
        )

        self.dx_to_zero_words = dx_to_zero_words
        self.dx_to_zero_words_arrow = arrow

    def name_derivative(self):
        deriv_words = OldTexText("``Derivative'' of $A$")
        deriv_words.scale(0.9)
        deriv_words.to_edge(UP+RIGHT)
        moving_group = VGroup(
            self.deriv_equation, 
            self.dx_to_zero_words,
            self.dx_to_zero_words_arrow,
        )
        moving_group.generate_target()
        moving_group.target.next_to(deriv_words, DOWN, LARGE_BUFF)
        moving_group.target.to_edge(RIGHT)

        self.play(
            FadeIn(deriv_words),
            MoveToTarget(moving_group)
        )

        dA_dx = VGroup(*self.deriv_equation[:3])
        box = Rectangle(color = GREEN)
        box.replace(dA_dx, stretch = True)
        box.scale(1.3)
        brace = Brace(box, UP)
        faders = VGroup(
            self.dx_to_zero_words[0],
            self.dx_to_zero_words_arrow
        )
        dx_to_zero = self.dx_to_zero_words[1]

        self.play(*list(map(FadeIn, [box, brace])))
        self.wait()
        self.play(
            FadeOut(faders),
            dx_to_zero.next_to, box, DOWN
        )
        self.wait()


    ########
    def show_smaller_x(self):
        return

    def shrink_dx(self, **kwargs):
        return
