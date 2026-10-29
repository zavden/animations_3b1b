# ==============================================================================
# Scene:      InvestedMoney
# Source:     videos/_2017/eoc/chapter5.py (lines 1723-1782)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InvestedMoney.py InvestedMoney -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InvestedMoney(Scene):
    def construct(self):
        # cash_str = "\\$\\$\\$"
        cash_str = "M"
        equation = OldTex(
            "{d", cash_str, "\\over", "dt}",
            "=", "(1 + r)", cash_str
        )
        equation.set_color_by_tex(cash_str, GREEN)
        equation.next_to(ORIGIN, LEFT)
        equation.to_edge(UP)

        arrow = Arrow(LEFT, RIGHT, color = WHITE)
        arrow.next_to(equation)

        solution = OldTex(
            cash_str, "(", "t", ")", "=", "e^", "{(1+r)", "t}"
        )
        solution.set_color_by_tex("t", YELLOW)
        solution.set_color_by_tex(cash_str, GREEN)
        solution.next_to(arrow, RIGHT)

        cash = OldTex("\\$")
        cash_pile = VGroup(*[
            cash.copy().shift(
                x*(1+MED_SMALL_BUFF)*cash.get_width()*RIGHT +\
                y*(1+MED_SMALL_BUFF)*cash.get_height()*UP
            )
            for x in range(40)
            for y in range(8)
        ])
        cash_pile.set_color(GREEN)
        cash_pile.center()
        cash_pile.shift(DOWN)

        anims = []
        cash_size = len(cash_pile)
        run_time = 10
        const = np.log(cash_size)/run_time
        for i, cash in enumerate(cash_pile):
            start_time = np.log(i+1)/const
            prop = start_time/run_time
            rate_func = squish_rate_func(
                smooth,
                np.clip(prop-0.5/run_time, 0, 1),
                np.clip(prop+0.5/run_time, 0, 1),
            )
            anims.append(GrowFromCenter(
                cash, rate_func = rate_func,
            ))

        self.add(equation)
        self.play(*anims, run_time = run_time)
        self.wait()
        self.play(ShowCreation(arrow))
        self.play(Write(solution, run_time = 2))
        self.wait()
        self.play(FadeOut(cash_pile))
        self.play(*anims, run_time = run_time)
        self.wait()
