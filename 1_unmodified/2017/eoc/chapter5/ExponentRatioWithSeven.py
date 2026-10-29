# ==============================================================================
# Scene:      ExponentRatioWithSeven
# Source:     videos/_2017/eoc/chapter5.py (lines 987-991)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExponentRatioWithSeven.py ExponentRatioWithSeven -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AnalyzeExponentRatio(PiCreatureScene):
    CONFIG = {
        "base" : 2,
        "base_str" : "2",
    }
    def construct(self):
        base_str = self.base_str

        func_def = OldTex("M(", "t", ")", "= ", "%s^"%base_str, "t")
        func_def.to_corner(UP+LEFT)
        self.add(func_def)

        ratio = OldTex(
            "{ {%s^"%base_str, "{t", "+", "dt}", "-", 
            "%s^"%base_str, "t}",
            "\\over \\,", "dt}"
        )
        ratio.shift(UP+LEFT)

        lhs = OldTex("{dM", "\\over \\,", "dt}", "(", "t", ")", "=")
        lhs.next_to(ratio, LEFT)


        two_to_t_plus_dt = VGroup(*ratio[:4])
        two_to_t = VGroup(*ratio[5:7])
        two_to_t_two_to_dt = OldTex(
            "%s^"%base_str, "t", 
            "%s^"%base_str, "{dt}"
        )
        two_to_t_two_to_dt.move_to(two_to_t_plus_dt, DOWN+LEFT)
        exp_prop_brace = Brace(two_to_t_two_to_dt, UP)

        one = OldTex("1")
        one.move_to(ratio[5], DOWN)
        lp, rp = parens = OldTex("()")
        parens.stretch(1.3, 1)
        parens.set_height(ratio.get_height())
        lp.next_to(ratio, LEFT, buff = 0)
        rp.next_to(ratio, RIGHT, buff = 0)

        extracted_two_to_t = OldTex("%s^"%base_str, "t")
        extracted_two_to_t.next_to(lp, LEFT, buff = SMALL_BUFF)

        expressions = [
            ratio, two_to_t_two_to_dt, 
            extracted_two_to_t, lhs, func_def
        ]
        for expression in expressions:
            expression.set_color_by_tex("t", YELLOW)
            expression.set_color_by_tex("dt", GREEN)

        #Apply exponential property
        self.play(
            Write(ratio), Write(lhs),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.wait(2)
        self.play(
            two_to_t_plus_dt.next_to, exp_prop_brace, UP,
            self.pi_creature.change_mode, "pondering"
        )
        self.play(
            ReplacementTransform(
                two_to_t_plus_dt.copy(), two_to_t_two_to_dt,
                run_time = 2,
                path_arc = np.pi,
            ),
            FadeIn(exp_prop_brace)
        )
        self.wait(2)

        #Talk about exponential property
        add_exp_rect, mult_rect = rects = [
            Rectangle(
                stroke_color = BLUE,
                stroke_width = 2,
            ).replace(mob).scale(1.1)
            for mob in [
                VGroup(*two_to_t_plus_dt[1:]),
                two_to_t_two_to_dt
            ]
        ]
        words = VGroup(*[
            OldTexText(s, " ideas")
            for s in ("Additive", "Multiplicative")
        ])
        words[0].move_to(words[1], LEFT)
        words.set_color(BLUE)
        words.next_to(two_to_t_plus_dt, RIGHT, buff = 1.5*LARGE_BUFF)
        arrows = VGroup(*[
            Arrow(word.get_left(), rect, color = words.get_color())
            for word, rect in zip(words, rects)
        ])

        self.play(ShowCreation(add_exp_rect))
        self.wait()
        self.play(ReplacementTransform(
            add_exp_rect.copy(), mult_rect
        ))
        self.wait()
        self.change_mode("happy")
        self.play(Write(words[0], run_time = 2))
        self.play(ShowCreation(arrows[0]))
        self.wait()
        self.play(
            Transform(*words),
            Transform(*arrows),
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [
            words[0], arrows[0], add_exp_rect, mult_rect,
            two_to_t_plus_dt, exp_prop_brace,
        ])))

        #Factor out 2^t
        self.play(*[
            FadeIn(
                mob,
                run_time = 2,
                rate_func = squish_rate_func(smooth, 0.5, 1)
            )
            for mob in (one, lp, rp)
        ] + [
            ReplacementTransform(
                mob, extracted_two_to_t,
                path_arc = np.pi/2,
                run_time = 2,
            )
            for mob in (two_to_t, VGroup(*two_to_t_two_to_dt[:2]))
        ] + [
            lhs.next_to, extracted_two_to_t, LEFT
        ])
        self.change_mode("pondering")
        shifter = VGroup(ratio[4], one, *two_to_t_two_to_dt[2:])
        stretcher = VGroup(lp, ratio[7], rp)
        self.play(
            shifter.next_to, ratio[7], UP,
            stretcher.stretch_in_place, 0.9, 0
        )
        self.wait(2)

        #Ask about dt -> 0
        brace = Brace(VGroup(extracted_two_to_t, ratio), DOWN)
        alt_brace = Brace(parens, DOWN)
        dt_to_zero = OldTex("dt", "\\to 0")
        dt_to_zero.set_color_by_tex("dt", GREEN)
        dt_to_zero.next_to(brace, DOWN)

        self.play(GrowFromCenter(brace))
        self.play(Write(dt_to_zero))
        self.wait(2)

        #Who cares
        randy = Randolph()
        randy.scale(0.7)
        randy.to_edge(DOWN)

        self.play(
            FadeIn(randy),
            self.pi_creature.change_mode, "plain",
        )
        self.play(PiCreatureSays(
            randy, "Who cares?", 
            bubble_config = {"direction" : LEFT},
            target_mode = "angry",
        ))
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(randy),
            FadeOut(randy),
            self.pi_creature.change_mode, "hooray",
            self.pi_creature.look_at, parens
        )
        self.play(
            Transform(brace, alt_brace),
            dt_to_zero.next_to, alt_brace, DOWN
        )
        self.wait()

        #Highlight separation
        rects = [
            Rectangle(
                stroke_color = color,
                stroke_width = 2,
            ).replace(mob, stretch = True).scale(1.1)
            for mob, color in [
                (VGroup(parens, dt_to_zero), GREEN), 
                (extracted_two_to_t, YELLOW),
            ]
        ]
        self.play(ShowCreation(rects[0]))
        self.wait(2)
        self.play(ReplacementTransform(rects[0].copy(), rects[1]))
        self.change_mode("happy")
        self.wait()
        self.play(*list(map(FadeOut, rects)))

        #Plug in specific values
        static_constant = self.try_specific_dt_values()
        constant = static_constant.copy()

        #Replace with actual constant
        limit_term = VGroup(
            brace, dt_to_zero, ratio[4], one, rects[0],
            *ratio[7:]+two_to_t_two_to_dt[2:]
        )
        self.play(FadeIn(rects[0]))
        self.play(limit_term.to_corner, DOWN+LEFT)
        self.play(
            lp.stretch, 0.5, 1,
            lp.stretch, 0.8, 0,
            lp.next_to, extracted_two_to_t[0], RIGHT,
            rp.stretch, 0.5, 1,
            rp.stretch, 0.8, 0,
            rp.next_to, lp, RIGHT, SMALL_BUFF,
            rp.shift, constant.get_width()*RIGHT,
            constant.next_to, extracted_two_to_t[0], RIGHT, MED_LARGE_BUFF
        )
        self.wait()
        self.change_mode("confused")
        self.wait()

        #Indicate distinction between dt group and t group again
        for mob in limit_term, extracted_two_to_t:
            self.play(FocusOn(mob))
            self.play(Indicate(mob))
        self.wait()

        #hold_final_value
        derivative = VGroup(
            lhs, extracted_two_to_t, parens, constant
        )
        func_def_rhs = VGroup(*func_def[-2:]).copy()
        func_lp, func_rp = func_parens = OldTex("()")
        func_parens.set_fill(opacity = 0)
        func_lp.next_to(func_def_rhs[0], LEFT, buff = 0)
        func_rp.next_to(func_lp, RIGHT, buff = func_def_rhs.get_width())
        func_def_rhs.add(func_parens)
        M = lhs[0][1]

        self.play(
            FadeOut(M),
            func_def_rhs.move_to, M, LEFT,
            func_def_rhs.set_fill, None, 1,
        )
        lhs[0].submobjects[1] = func_def_rhs
        self.wait()
        self.play(
            derivative.next_to, self.pi_creature, UP,
            derivative.to_edge, RIGHT,
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.wait(2)
        for mob in extracted_two_to_t, constant:
            self.play(Indicate(mob))
            self.wait()
        self.wait(2)

    def try_specific_dt_values(self):
        expressions = []
        for num_zeros in [1, 2, 4, 7]:
            dt_str = "0." + num_zeros*"0" + "1"
            dt_num = float(dt_str)
            output_num = (self.base**dt_num - 1) / dt_num
            output_str = "%.7f\\dots"%output_num

            expression = OldTex(
                "{%s^"%self.base_str, "{%s}"%dt_str, "-1", 
                "\\over \\,", "%s}"%dt_str, 
                "=", output_str
            )
            expression.set_color_by_tex(dt_str, GREEN)
            expression.set_color_by_tex(output_str, BLUE)
            expression.to_corner(UP+RIGHT)
            expressions.append(expression)

        curr_expression = expressions[0]
        self.play(
            Write(curr_expression),
            self.pi_creature.change_mode, "pondering"
        )
        self.wait(2)
        for expression in expressions[1:]:
            self.play(Transform(curr_expression, expression))
            self.wait(2)
        return curr_expression[-1]


class ExponentRatioWithSeven(AnalyzeExponentRatio):
    CONFIG = {
        "base" : 7,
        "base_str" : "7",
    }
