# ==============================================================================
# Scene:      NaturalLog
# Source:     videos/_2017/eoc/chapter5.py (lines 1784-1879)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NaturalLog.py NaturalLog -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
# ==============================================================================

from manim_imports_ext import *

class NaturalLog(Scene):
    def construct(self):
        expressions = VGroup(*list(map(self.get_expression, [2, 3, 7])))
        expressions.arrange(DOWN, buff = MED_SMALL_BUFF)
        expressions.to_edge(LEFT)

        self.play(FadeIn(
            expressions, 
            run_time = 3, 
            lag_ratio = 0.5
        ))
        self.wait()
        self.play(
            expressions.set_fill, None, 1,
            run_time = 2,
            lag_ratio = 0.5
        )
        self.wait()
        for i in 0, 2, 1:
            self.show_natural_loggedness(expressions[i])

    def show_natural_loggedness(self, expression):
        base, constant = expression[1], expression[-3]

        log_constant, exp_constant = constant.copy(), constant.copy()
        log_base, exp_base = base.copy(), base.copy()
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        log_equals, exp_equals = list(map(OldTex, "=="))

        ln = OldTex("\\ln(2)")
        log_base.move_to(ln[-2])        
        ln.remove(ln[-2])
        log_equals.next_to(ln, LEFT)
        log_constant.next_to(log_equals, LEFT)
        log_expression = VGroup(
            ln, log_constant, log_equals, log_base
        )

        e = OldTex("e")
        exp_constant.scale(0.7)
        exp_constant.next_to(e, UP+RIGHT, buff = 0)
        exp_base.next_to(exp_equals, RIGHT)
        VGroup(exp_base, exp_equals).next_to(
            VGroup(e, exp_constant), RIGHT, 
            aligned_edge = DOWN
        )
        exp_expression = VGroup(
            e, exp_constant, exp_equals, exp_base
        )

        for group, vect in (log_expression, UP), (exp_expression, DOWN):
            group.to_edge(RIGHT)
            group.shift(vect)

        self.play(
            ReplacementTransform(base.copy(), log_base),
            ReplacementTransform(constant.copy(), log_constant),
            run_time = 2
        )
        self.play(Write(ln), Write(log_equals))
        self.wait()
        self.play(
            ReplacementTransform(
                log_expression.copy(),
                exp_expression,
                run_time = 2,
            )
        )
        self.wait(2)

        ln_a = expression[-1]
        self.play(
            FadeOut(expression[-2]),
            FadeOut(constant),
            ln_a.move_to, constant, LEFT,
            ln_a.set_color, BLUE
        )
        self.wait()
        self.play(*list(map(FadeOut, [log_expression, exp_expression])))
        self.wait()

    def get_expression(self, base):
        expression = OldTex(
            "{d(", "%d^"%base, "t", ")", "\\over \\,", "dt}",
            "=", "%d^"%base, "t", "(%.4f\\dots)"%np.log(base),
        )
        expression.set_color_by_tex("t", YELLOW)
        expression.set_color_by_tex("dt", GREEN)
        expression.set_color_by_tex("\\dots", BLUE)

        brace = Brace(expression.get_part_by_tex("\\dots"), UP)
        brace_text = brace.get_text("$\\ln(%d)$"%base)
        for mob in brace, brace_text:
            mob.set_fill(opacity = 0)

        expression.add(brace, brace_text)
        return expression
