# ==============================================================================
# Scene:      WhyNaturalLogOf2ShowsUp
# Source:     videos/_2017/eoc/chapter5.py (lines 1377-1519)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyNaturalLogOf2ShowsUp.py WhyNaturalLogOf2ShowsUp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyNaturalLogOf2ShowsUp(TeacherStudentsScene):
    def construct(self):
        self.add_e_to_the_three_t()
        self.show_e_to_log_2()

    def add_e_to_the_three_t(self):
        exp_c = self.get_exp_C("c")
        exp_c.next_to(self.teacher, UP+LEFT)

        self.play(
            FadeIn(
                exp_c, 
                run_time = 2, 
                lag_ratio = 0.5
            ),
            self.teacher.change, "raise_right_hand"
        )
        self.wait()
        self.look_at(4*LEFT + UP)
        self.wait(3)

        self.exp_c = exp_c

    def show_e_to_log_2(self):
        equation = OldTex(
            "2", "^t", "= e^", "{\\ln(2)", "t}"
        )
        equation.move_to(self.exp_c)
        t_group = equation.get_parts_by_tex("t")
        non_t_group = VGroup(*equation)
        non_t_group.remove(*t_group)

        log_words = OldTexText("``$e$ to the ", "\\emph{what}", "equals 2?''")
        log_words.set_color_by_tex("what", BLUE)
        log_words.next_to(equation, UP+LEFT)
        log_words_arrow = Arrow(
            log_words.get_right(),
            equation.get_part_by_tex("ln(2)").get_corner(UP+LEFT),
            color = BLUE,
        )

        derivative = OldTex(
            "\\ln(2)", "2", "^t", "=", "\\ln(2)", "e^", "{\\ln(2)", "t}"
        )
        derivative.move_to(equation)
        for tex_mob in equation, derivative:
            tex_mob.set_color_by_tex("ln(2)", BLUE)
            tex_mob.set_color_by_tex("t", YELLOW)
        derivative_arrow = Arrow(1.5*UP, ORIGIN, buff = 0)
        derivative_arrow.set_color(WHITE)
        derivative_arrow.next_to(
            derivative.get_parts_by_tex("="), UP
        )
        derivative_symbol = OldTexText("Derivative")
        derivative_symbol.next_to(derivative_arrow, RIGHT)

        self.play(
            Write(non_t_group),
            self.exp_c.next_to, equation, LEFT, 2*LARGE_BUFF,
            self.exp_c.to_edge, UP,
        )
        self.play_student_changes("confused", "sassy", "erm")
        self.play(
            Write(log_words),
            ShowCreation(
                log_words_arrow, 
                run_time = 2,
                rate_func = squish_rate_func(smooth, 0.5, 1)
            )
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = log_words
        )
        self.wait(2)

        t_group.save_state()
        t_group.shift(UP)
        t_group.set_fill(opacity = 0)
        self.play(
            ApplyMethod(
                t_group.restore,
                run_time = 2,
                lag_ratio = 0.5,
            ),
            self.teacher.change_mode, "speaking"
        )
        self.wait(2)
        self.play(FocusOn(self.exp_c))
        self.play(Indicate(self.exp_c, scale_factor = 1.05))
        self.wait(2)

        self.play(
            equation.next_to, derivative_arrow, UP,
            equation.shift, MED_SMALL_BUFF*RIGHT,
            FadeOut(VGroup(log_words, log_words_arrow)),
            self.teacher.change_mode, "raise_right_hand",
        )
        self.play(
            ShowCreation(derivative_arrow),
            Write(derivative_symbol),
            Write(derivative)
        )
        self.wait(3)
        self.play(self.teacher.change_mode, "happy")
        self.wait(2)

        student = self.get_students()[1]
        ln = derivative.get_part_by_tex("ln(2)").copy()
        rhs = OldTex("=%s"%self.get_log_str(2))
        self.play(
            ln.next_to, student, UP+LEFT, MED_LARGE_BUFF,
            student.change_mode, "raise_left_hand",
        )
        rhs.next_to(ln, RIGHT)
        self.play(Write(rhs))
        self.wait(2)


    ######

    def get_exp_C(self, C):
        C_str = str(C)
        result = OldTex(
            "{d(", "e^", "{%s"%C_str, "t}", ")", "\\over", "dt}",
            "=", C_str, "e^", "{%s"%C_str, "t}",
        )
        result.set_color_by_tex(C_str, BLUE)
        result.C_str = C_str
        return result

    def get_a_to_t(self, a):
        a_str = str(a)
        log_str = self.get_log_str(a)
        result = OldTex(
            "{d(", a_str, "^t", ")", "\\over", "dt}",
            "=", log_str, a_str, "^t"
        )
        result.set_color_by_tex(log_str, BLUE)
        return result

    def get_log_str(self, a):
        return "%.4f\\dots"%np.log(float(a))
