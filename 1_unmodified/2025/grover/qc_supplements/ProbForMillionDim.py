# ==============================================================================
# Scene:      ProbForMillionDim
# Source:     videos/_2025/grover/qc_supplements.py (lines 1013-1044)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProbForMillionDim.py ProbForMillionDim -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProbForMillionDim(InteractiveScene):
    def construct(self):
        # Context
        context = VGroup(
            Tex(R"N = 2^{20}"),
            TexText(R"\# Reps: 804"),
        )
        context.arrange(DOWN, aligned_edge=LEFT)
        context.to_corner(UL)

        # Prob
        theta = math.asin(2**(-10))
        prob = math.sin((2 * 804 + 1) * theta)**2

        chance_lhs = Tex(R"P(k) = ", t2c={"k": YELLOW})
        chance_rhs = DecimalNumber(100 * prob, num_decimal_places=7, unit="%")
        chance_rhs.next_to(chance_lhs, RIGHT, SMALL_BUFF).shift(0.05 * UR)
        chance = VGroup(chance_lhs, chance_rhs)
        chance.scale(1.25)
        chance.to_edge(RIGHT)

        brace = Brace(chance_rhs, DOWN)
        equation = brace.get_tex(R"\sin((2 \cdot 804 + 1) \theta)^2")
        equation.set_color(GREY_C)
        equation.scale(0.7, about_edge=UP)

        self.play(Write(chance))
        self.play(
            GrowFromCenter(brace),
            FadeIn(equation),
        )
        self.wait()
