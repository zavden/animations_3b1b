# ==============================================================================
# Scene:      LimitJustMeansApproach
# Source:     videos/_2017/eoc/chapter7.py (lines 78-149)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LimitJustMeansApproach.py LimitJustMeansApproach -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class LimitJustMeansApproach(PiCreatureScene):
    CONFIG = {
        "dx_color" : GREEN,
        "max_num_zeros" : 7,
    }
    def construct(self):
        limit_expression = self.get_limit_expression()
        limit_expression.shift(2*LEFT)
        limit_expression.to_edge(UP)

        evaluated_expressions = self.get_evaluated_expressions()
        evaluated_expressions.next_to(limit_expression, DOWN, buff = LARGE_BUFF)
        brace = Brace(evaluated_expressions[0][-1], DOWN)
        question = OldTexText("What does this ``approach''?")
        question.next_to(brace, DOWN)

        point = VectorizedPoint(limit_expression.get_right())
        expression = VGroup(
            limit_expression[1].copy(), 
            point, point.copy()
        )
        self.add(limit_expression)
        self.change_mode("raise_right_hand")
        for next_expression in evaluated_expressions:
            next_expression.move_to(evaluated_expressions[0], RIGHT)
            self.play(
                Transform(
                    expression, next_expression,
                    lag_ratio = 0.5,
                ),
                self.pi_creature.look_at, next_expression[-1]
            )
            if brace not in self.get_mobjects():
                self.play(
                    GrowFromCenter(brace),
                    Write(question)
                )
            self.wait(0.5)
        self.wait(2)

    def create_pi_creature(self):
        self.pi_creature = Mortimer().flip()
        self.pi_creature.to_corner(DOWN+LEFT)
        return self.pi_creature

    def get_limit_expression(self):
        lim = OldTex("\\lim_", "{dx", " \\to 0}")
        lim.set_color_by_tex("dx", self.dx_color)
        ratio = self.get_expression("dx")
        ratio.next_to(lim, RIGHT)
        limit_expression = VGroup(lim, ratio)
        return limit_expression

    def get_evaluated_expressions(self):
        result = VGroup()
        for num_zeros in range(1, self.max_num_zeros+1):
            dx_str = "0." + "0"*num_zeros + "1"
            expression = self.get_expression(dx_str)            
            dx = float(dx_str)
            ratio = ((2+dx)**3-2**3)/dx
            ratio_mob = OldTex("%.6f\\dots"%ratio)
            group = VGroup(expression, OldTex("="), ratio_mob)
            group.arrange(RIGHT)
            result.add(group)
        return result

    def get_expression(self, dx):
        result = OldTex(
            "{(2 + ", str(dx), ")^3 - 2^3 \\over", str(dx)
        )
        result.set_color_by_tex(dx, self.dx_color)
        return result
