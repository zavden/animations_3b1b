# ==============================================================================
# Scene:      LightweightLadderScene
# Source:     videos/_2017/eoc/chapter6.py (lines 1208-1215)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LightweightLadderScene.py LightweightLadderScene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL Prism takes (width, height, depth, color=...); Cairo took dimensions=[...], fill_color=...
#   - GL Prism is a Surface group, not a VMobject: DrawBorderThenFill asserts; FadeIn it
#   - np.array(VGroup) is ragged in numpy 2: pick the parts with a comprehension
# ==============================================================================

from manim_imports_ext import *

class Ladder(VMobject):
    CONFIG = {
        "height" : 4,
        "width" : 1,
        "n_rungs" : 7,
    }
    def init_points(self):
        left_line, right_line = [
            Line(ORIGIN, self.height*UP).shift(self.width*vect/2.0)
            for vect in (LEFT, RIGHT)
        ]
        rungs = [
            Line(
                left_line.point_from_proportion(a),
                right_line.point_from_proportion(a),
            )
            for a in np.linspace(0, 1, 2*self.n_rungs+1)[1:-1:2]
        ]
        self.add(left_line, right_line, *rungs)
        self.center()


class RelatedRatesExample(ThreeDScene):
    CONFIG = {
        "start_x" : 3.0,
        "start_y" : 4.0,
        "wall_dimensions" : [0.3, 5, 5],
        "wall_color" : color_gradient([GREY_BROWN, BLACK], 4)[1],
        "wall_center" : 1.5*LEFT+0.5*UP,
    }
    def construct(self):
        self.introduce_ladder()
        self.write_related_rates()
        self.measure_ladder()
        self.slide_ladder()
        self.ponder_question()
        self.write_equation()
        self.isolate_x_of_t()
        self.discuss_lhs_as_function()
        self.let_dt_pass()
        self.take_derivative_of_rhs()
        self.take_derivative_of_lhs()
        self.bring_back_velocity_arrows()
        self.replace_terms_in_final_form()
        self.write_final_solution()

    def introduce_ladder(self):
        ladder = Ladder(height = self.get_ladder_length())

        # CHANGE: GL Prism takes (width, height, depth, color=...); Cairo took dimensions=[...], fill_color=...
        wall = Prism(
            *self.wall_dimensions,
            color = self.wall_color,
            opacity = 1,
        )
        wall.rotate(np.pi/12, UP)
        wall.shift(self.wall_center)

        ladder.generate_target()
        ladder.fallen = ladder.copy()
        ladder.target.rotate(self.get_ladder_angle(), LEFT)
        ladder.fallen.rotate(np.pi/2, LEFT)
        for ladder_copy in ladder.target, ladder.fallen:
            ladder_copy.rotate(-5*np.pi/12, UP)
            ladder_copy.next_to(wall, LEFT, 0, DOWN)
            ladder_copy.shift(0.8*RIGHT) ##BAD!


        self.play(
            ShowCreation(ladder, run_time = 2)
        )
        self.wait()

        self.play(
            # CHANGE: GL Prism is a Surface group, not a VMobject: DrawBorderThenFill asserts; FadeIn it
            FadeIn(wall),
            MoveToTarget(ladder),
            run_time = 2
        )
        self.wait()

        self.ladder = ladder

    def write_related_rates(self):
        words = OldTexText("Related rates")
        words.to_corner(UP+RIGHT)
        self.play(Write(words))
        self.wait()

        self.related_rates_words = words

    def measure_ladder(self):
        ladder = self.ladder
        ladder_brace = self.get_ladder_brace(ladder)

        x_and_y_lines = self.get_x_and_y_lines(ladder)
        x_line, y_line = x_and_y_lines

        y_label = OldTex("%dm"%int(self.start_y))
        y_label.next_to(y_line, LEFT, buff = SMALL_BUFF)
        y_label.set_color(y_line.get_color())

        x_label = OldTex("%dm"%int(self.start_x))
        x_label.next_to(x_line, UP)
        x_label.set_color(x_line.get_color())

        self.play(Write(ladder_brace))
        self.wait()
        self.play(ShowCreation(y_line), Write(y_label))
        self.wait()
        self.play(ShowCreation(x_line), Write(x_label))
        self.wait(2)
        self.play(*list(map(FadeOut, [x_label, y_label])))

        self.ladder_brace = ladder_brace
        self.x_and_y_lines = x_and_y_lines
        self.numerical_x_and_y_labels = VGroup(x_label, y_label)

    def slide_ladder(self):
        ladder = self.ladder
        brace = self.ladder_brace
        x_and_y_lines = self.x_and_y_lines
        x_line, y_line = x_and_y_lines

        down_arrow, left_arrow = [
            Arrow(ORIGIN, vect, color = YELLOW, buff = 0)
            for vect in (DOWN, LEFT)
        ]
        down_arrow.shift(y_line.get_start()+MED_SMALL_BUFF*RIGHT)
        left_arrow.shift(x_line.get_start()+SMALL_BUFF*DOWN)

        # speed_label = OldTex("1 \\text{m}/\\text{s}")
        speed_label = OldTex("1 \\frac{\\text{m}}{\\text{s}}")
        speed_label.next_to(down_arrow, RIGHT, buff = SMALL_BUFF)

        q_marks = OldTex("???")
        q_marks.next_to(left_arrow, DOWN, buff = SMALL_BUFF)


        added_anims = [
            UpdateFromFunc(brace, self.update_brace),
            UpdateFromFunc(x_and_y_lines, self.update_x_and_y_lines),
            Animation(down_arrow),
        ]
        self.play(ShowCreation(down_arrow))
        self.play(Write(speed_label))
        self.let_ladder_fall(ladder, *added_anims)
        self.wait()
        self.reset_ladder(ladder, *added_anims)
        self.play(ShowCreation(left_arrow))
        self.play(Write(q_marks))
        self.wait()
        self.let_ladder_fall(ladder, *added_anims)
        self.wait()
        self.reset_ladder(ladder, *added_anims)
        self.wait()

        self.dy_arrow = down_arrow
        self.dy_label = speed_label
        self.dx_arrow = left_arrow
        self.dx_label = q_marks

    def ponder_question(self):
        randy = Randolph(mode = "pondering")
        randy.flip()
        randy.to_corner(DOWN+RIGHT)

        self.play(FadeIn(randy))
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.change_mode, "confused",
            randy.look_at, self.ladder.get_top()
        )
        self.play(randy.look_at, self.ladder.get_bottom())
        self.play(randy.look_at, self.ladder.get_top())
        self.play(Blink(randy))
        self.wait()
        self.play(PiCreatureSays(
            randy, "Give names"
        ))
        self.play(Blink(randy))
        self.play(*list(map(FadeOut, [
            randy, randy.bubble, randy.bubble.content
        ])))

    def write_equation(self):
        self.x_and_y_labels = self.get_x_and_y_labels()
        x_label, y_label = self.x_and_y_labels

        equation = OldTex(
            "x(t)", "^2", "+", "y(t)", "^2", "=", "5^2"
        )
        equation[0].set_color(GREEN)
        equation[3].set_color(RED)
        equation.next_to(self.related_rates_words, DOWN, buff = MED_LARGE_BUFF)
        equation.to_edge(RIGHT, buff = LARGE_BUFF)

        self.play(Write(y_label))
        self.wait()
        self.let_ladder_fall(
            self.ladder,
            y_label.shift, self.start_y*DOWN/2,
            *self.get_added_anims_for_ladder_fall()[:-1],
            rate_func = lambda t : 0.2*there_and_back(t),
            run_time = 3
        )
        self.play(FocusOn(x_label))
        self.play(Write(x_label))
        self.wait(2)
        self.play(
            ReplacementTransform(x_label.copy(), equation[0]),
            ReplacementTransform(y_label.copy(), equation[3]),
            # CHANGE: np.array(VGroup) is ragged in numpy 2: pick the parts with a comprehension
            Write(VGroup(*[equation[i] for i in (1, 2, 4, 5, 6)]))
        )
        self.wait(2)
        self.let_ladder_fall(
            self.ladder,
            *self.get_added_anims_for_ladder_fall(),
            rate_func = there_and_back,
            run_time = 6
        )
        self.wait()

        self.equation = equation

    def isolate_x_of_t(self):
        alt_equation = OldTex(
            "x(t)", "=", "\\big(5^2", "-", "y(t)", "^2 \\big)", "^{1/2}",
        )
        alt_equation[0].set_color(GREEN)
        alt_equation[4].set_color(RED)
        alt_equation.next_to(self.equation, DOWN, buff = MED_LARGE_BUFF)
        alt_equation.to_edge(RIGHT)

        randy = Randolph()
        randy.next_to(
            alt_equation, DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT,
        )
        randy.look_at(alt_equation)

        find_dx_dt = OldTex("\\text{Find } \\,", "\\frac{dx}{dt}")
        find_dx_dt.next_to(randy, RIGHT, aligned_edge = UP)
        find_dx_dt[1].set_color(GREEN)

        self.play(FadeIn(randy))
        self.play(
            randy.change_mode, "raise_right_hand", 
            randy.look_at, alt_equation,
            *[
                ReplacementTransform(
                    self.equation[i].copy(), 
                    alt_equation[j],
                    path_arc = np.pi/2,
                    run_time = 3,
                    rate_func = squish_rate_func(
                        smooth, j/12.0, (j+6)/12.0
                    )
                )
                for i, j in enumerate([0, 6, 3, 4, 5, 1, 2])
            ]
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            Write(find_dx_dt),
            randy.change_mode, "pondering",
            randy.look_at, find_dx_dt,
        )
        self.let_ladder_fall(
            self.ladder, *self.get_added_anims_for_ladder_fall(),
            run_time = 8,
            rate_func = there_and_back
        )
        self.play(*list(map(FadeOut, [
            randy, find_dx_dt, alt_equation
        ])))
        self.wait()

    def discuss_lhs_as_function(self):
        equation = self.equation
        lhs = VGroup(*equation[:5])
        brace = Brace(lhs, DOWN)
        function_of_time = brace.get_text(
            "Function of time"
        )
        constant_words = OldTexText(
            """that happens to
            be constant"""
        )
        constant_words.set_color(YELLOW)
        constant_words.next_to(function_of_time, DOWN)

        derivative = OldTex(
            "\\frac{d\\left(x(t)^2 + y(t)^2 \\right)}{dt}"
        )
        derivative.next_to(equation, DOWN, buff = MED_LARGE_BUFF)
        derivative.shift( ##Align x terms
            equation[0][0].get_center()[0]*RIGHT-\
            derivative[2].get_center()[0]*RIGHT
        )
        derivative_interior = lhs.copy()
        derivative_interior.move_to(VGroup(*derivative[2:13]))
        derivative_scaffold = VGroup(
            *list(derivative[:2])+list(derivative[13:])
        )

        self.play(
            GrowFromCenter(brace),
            Write(function_of_time)
        )
        self.wait()
        self.play(Write(constant_words))
        self.let_ladder_fall(
            self.ladder, *self.get_added_anims_for_ladder_fall(),
            run_time = 6,
            rate_func = lambda t : 0.5*there_and_back(t)
        )
        self.wait()
        self.play(*list(map(FadeOut, [
            brace, constant_words, function_of_time
        ])))
        self.play(
            ReplacementTransform(lhs.copy(), derivative_interior),
            Write(derivative_scaffold),
        )
        self.wait()

        self.derivative = VGroup(
            derivative_scaffold, derivative_interior
        )

    def let_dt_pass(self):
        dt_words = OldTexText("After", "$dt$", "seconds...")
        dt_words.to_corner(UP+LEFT)
        dt = dt_words[1]
        dt.set_color(YELLOW)
        dt_brace = Brace(dt, buff = SMALL_BUFF)
        dt_brace_text = dt_brace.get_text("Think 0.01", buff = SMALL_BUFF)
        dt_brace_text.set_color(dt.get_color())

        shadow_ladder = self.ladder.copy()
        shadow_ladder.fade(0.5)

        x_line, y_line = self.x_and_y_lines
        y_top = y_line.get_start()
        x_left = x_line.get_start()

        self.play(Write(dt_words, run_time = 2))
        self.play(
            GrowFromCenter(dt_brace),
            Write(dt_brace_text, run_time = 2)
        )
        self.play(*list(map(FadeOut, [
            self.dy_arrow, self.dy_label, 
            self.dx_arrow, self.dx_label, 
        ])))
        self.add(shadow_ladder)
        self.let_ladder_fall(
            self.ladder, *self.get_added_anims_for_ladder_fall(),
            rate_func = lambda t : 0.1*smooth(t),
            run_time = 1
        )

        new_y_top = y_line.get_start()
        new_x_left = x_line.get_start()

        dy_line = Line(y_top, new_y_top)
        dy_brace = Brace(dy_line, RIGHT, buff = SMALL_BUFF)
        dy_label = dy_brace.get_text("$dy$", buff = SMALL_BUFF)
        dy_label.set_color(RED)

        dx_line = Line(x_left, new_x_left)
        dx_brace = Brace(dx_line, DOWN, buff = SMALL_BUFF)
        dx_label = dx_brace.get_text("$dx$")
        dx_label.set_color(GREEN)

        VGroup(dy_line, dx_line).set_color(YELLOW)

        for line, brace, label in (dy_line, dy_brace, dy_label), (dx_line, dx_brace, dx_label):
            self.play(
                ShowCreation(line),
                GrowFromCenter(brace),
                Write(label),
                run_time = 1
            )
        self.wait()
        self.play(Indicate(self.derivative[1]))
        self.wait()

        self.dy_group = VGroup(dy_line, dy_brace, dy_label)
        self.dx_group = VGroup(dx_line, dx_brace, dx_label)
        self.shadow_ladder = shadow_ladder

    def take_derivative_of_rhs(self):
        derivative = self.derivative
        equals_zero = OldTex("= 0")
        equals_zero.next_to(derivative)

        rhs = self.equation[-1]

        self.play(Write(equals_zero))
        self.wait()
        self.play(FocusOn(rhs))
        self.play(Indicate(rhs))
        self.wait()
        self.reset_ladder(
            self.ladder, 
            *self.get_added_anims_for_ladder_fall()+[
                Animation(self.dy_group),
                Animation(self.dx_group),
            ],
            rate_func = there_and_back,
            run_time = 3
        )
        self.wait()

        self.equals_zero = equals_zero

    def take_derivative_of_lhs(self):
        derivative_scaffold, equation = self.derivative
        equals_zero_copy = self.equals_zero.copy()

        lhs_derivative = OldTex(
            "2", "x(t)", "\\frac{dx}{dt}", "+",
            "2", "y(t)", "\\frac{dy}{dt}",
        )
        lhs_derivative[1].set_color(GREEN)
        VGroup(*lhs_derivative[2][:2]).set_color(GREEN)
        lhs_derivative[5].set_color(RED)
        VGroup(*lhs_derivative[6][:2]).set_color(RED)
        lhs_derivative.next_to(
            derivative_scaffold, DOWN,
            aligned_edge = RIGHT,
            buff = MED_LARGE_BUFF
        )
        equals_zero_copy.next_to(lhs_derivative, RIGHT)

        pairs = [
            (0, 1), (1, 0), #x^2 -> 2x
            (2, 3), (3, 5), (4, 4), #+y^2 -> +2y
        ]
        def perform_replacement(index_pairs):
            self.play(*[
                ReplacementTransform(
                    equation[i].copy(), lhs_derivative[j],
                    path_arc = np.pi/2,
                    run_time = 2
                )
                for i, j in index_pairs
            ])

        perform_replacement(pairs[:2])
        self.play(Write(lhs_derivative[2]))
        self.wait()
        self.play(Indicate(
            VGroup(
                *list(lhs_derivative[:2])+\
                list(lhs_derivative[2][:2])
            ),
            run_time = 2
        ))
        self.play(Indicate(VGroup(*lhs_derivative[2][3:])))
        self.wait(2)
        perform_replacement(pairs[2:])
        self.play(Write(lhs_derivative[6]))
        self.wait()

        self.play(FocusOn(self.equals_zero))
        self.play(ReplacementTransform(
            self.equals_zero.copy(),
            equals_zero_copy
        ))
        self.wait(2)

        lhs_derivative.add(equals_zero_copy)
        self.lhs_derivative = lhs_derivative

    def bring_back_velocity_arrows(self):
        dx_dy_group = VGroup(self.dx_group, self.dy_group)
        arrow_group = VGroup(
            self.dy_arrow, self.dy_label,
            self.dx_arrow, self.dx_label,
        )
        ladder_fall_args = [self.ladder] + self.get_added_anims_for_ladder_fall()


        self.reset_ladder(*ladder_fall_args + [
            FadeOut(dx_dy_group),
            FadeOut(self.derivative),
            FadeOut(self.equals_zero),
            self.lhs_derivative.shift, 2*UP,
        ])
        self.remove(self.shadow_ladder)
        self.play(FadeIn(arrow_group))
        self.let_ladder_fall(*ladder_fall_args)
        self.wait()
        self.reset_ladder(*ladder_fall_args)
        self.wait()

    def replace_terms_in_final_form(self):
        x_label, y_label = self.x_and_y_labels
        num_x_label, num_y_label = self.numerical_x_and_y_labels

        new_lhs_derivative = OldTex(
            "2", "(%d)"%int(self.start_x), "\\frac{dx}{dt}", "+",
            "2", "(%d)"%int(self.start_y), "(-1)",
            "= 0"
        )
        new_lhs_derivative[1].set_color(GREEN)
        VGroup(*new_lhs_derivative[2][:2]).set_color(GREEN)
        new_lhs_derivative[5].set_color(RED)
        new_lhs_derivative.next_to(
            self.lhs_derivative, DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = RIGHT
        )
        def fill_in_equation_part(*indices):
            self.play(*[
                ReplacementTransform(
                    self.lhs_derivative[i].copy(),
                    new_lhs_derivative[i],
                    run_time = 2
                )
                for i in indices
            ])

        self.play(FadeOut(y_label), FadeIn(num_y_label))
        fill_in_equation_part(3, 4, 5)
        self.play(FadeOut(x_label), FadeIn(num_x_label))
        for indices in [(0, 1), (6,), (2, 7)]:
            fill_in_equation_part(*indices)
            self.wait()
        self.wait()

        self.new_lhs_derivative = new_lhs_derivative

    def write_final_solution(self):
        solution = OldTex(
            "\\frac{dx}{dt} = \\frac{4}{3}"
        )
        for i in 0, 1, -1:
            solution[i].set_color(GREEN)
        solution[-3].set_color(RED)
        solution.next_to(
            self.new_lhs_derivative, DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = RIGHT
        )

        box = Rectangle(color = YELLOW)
        box.replace(solution)
        box.scale(1.5)

        self.play(Write(solution))
        self.wait()
        self.play(ShowCreation(box))
        self.wait()

    #########

    def get_added_anims_for_ladder_fall(self):
        return [
            UpdateFromFunc(self.ladder_brace, self.update_brace),
            UpdateFromFunc(self.x_and_y_lines, self.update_x_and_y_lines),
            UpdateFromFunc(self.x_and_y_labels, self.update_x_and_y_labels),
        ]

    def let_ladder_fall(self, ladder, *added_anims, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", self.start_y)
        kwargs["rate_func"] = kwargs.get("rate_func", None)
        self.play(
            Transform(ladder, ladder.fallen),
            *added_anims,
            **kwargs
        )

    def reset_ladder(self, ladder, *added_anims, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 2)
        self.play(
            Transform(ladder, ladder.target),
            *added_anims,
            **kwargs
        )

    def update_brace(self, brace):
        Transform(
            brace, self.get_ladder_brace(self.ladder)
        ).update(1)
        return brace

    def update_x_and_y_lines(self, x_and_y_lines):
        Transform(
            x_and_y_lines,
            self.get_x_and_y_lines(self.ladder)
        ).update(1)
        return x_and_y_lines

    def update_x_and_y_labels(self, x_and_y_labels):
        Transform(
            x_and_y_labels,
            self.get_x_and_y_labels()
        ).update(1)
        return x_and_y_labels

    def get_ladder_brace(self, ladder):
        vect = rotate_vector(LEFT, -self.get_ladder_angle())
        brace = Brace(ladder, vect)        
        length_string = "%dm"%int(self.get_ladder_length())
        length_label = brace.get_text(
            length_string, use_next_to = False
        )
        brace.add(length_label)
        brace.length_label = length_label
        return brace

    def get_x_and_y_labels(self):
        x_line, y_line = self.x_and_y_lines

        x_label = OldTex("x(t)")
        x_label.set_color(x_line.get_color())
        x_label.next_to(x_line, DOWN, buff = SMALL_BUFF)

        y_label = OldTex("y(t)")
        y_label.set_color(y_line.get_color())
        y_label.next_to(y_line, LEFT, buff = SMALL_BUFF)

        return VGroup(x_label, y_label)

    def get_x_and_y_lines(self, ladder):
        bottom_point, top_point = np.array(ladder[1].get_start_and_end())
        interim_point = top_point[0]*RIGHT + bottom_point[1]*UP
        interim_point += SMALL_BUFF*DOWN
        y_line = Line(top_point, interim_point)
        y_line.set_color(RED)
        x_line = Line(bottom_point, interim_point)
        x_line.set_color(GREEN)

        return VGroup(x_line, y_line)

    def get_ladder_angle(self):
        if hasattr(self, "ladder"):
            c1 = self.ladder.get_corner(UP+RIGHT)
            c2 = self.ladder.get_corner(DOWN+LEFT)
            vect = c1-c2
            return np.pi/2 - angle_of_vector(vect)
        else:
            return np.arctan(self.start_x/self.start_y)

    def get_ladder_length(self):
        return get_norm([self.start_x, self.start_y])


class LightweightLadderScene(RelatedRatesExample):
    CONFIG = {
        "skip_animations" : True
    }
    def construct(self):
        self.introduce_ladder()
        self.measure_ladder()
        self.add(self.numerical_x_and_y_labels)
