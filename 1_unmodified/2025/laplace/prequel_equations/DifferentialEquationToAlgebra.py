# ==============================================================================
# Scene:      DifferentialEquationToAlgebra
# Source:     videos/_2025/laplace/prequel_equations.py (lines 1587-1616)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DifferentialEquationToAlgebra.py DifferentialEquationToAlgebra -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DifferentialEquationToAlgebra(InteractiveScene):
    def construct(self):
        # Associations
        t2c = {"{s}": YELLOW}
        arrow = Vector(1.5 * RIGHT, thickness=5)
        words = VGroup(Text("ODE"), Text("Algebra"))
        symbols = VGroup(Tex(R"d / dt"), Tex(R"\times {s}", t2c=t2c))
        for group in words, symbols:
            for mob, vect in zip(group, [LEFT, RIGHT]):
                mob.next_to(arrow, vect)

        deriv_eq = Tex(R"\frac{d}{dt} e^{{s}t} = {s} e^{{s} t}", t2c=t2c, font_size=36)
        deriv_eq.next_to(arrow, UP, buff=0.25)

        self.play(LaggedStart(
            FadeIn(words[0], lag_ratio=0.1),
            GrowArrow(arrow),
            FadeIn(words[1], 0.25 * RIGHT),
        ))
        self.wait()
        self.play(
            FadeOut(words[0], 0.5 * UP),
            FadeIn(symbols[0], 0.5 * UP),
            FadeIn(deriv_eq)
        )
        self.play(
            FadeOut(words[1], 0.5 * UP),
            FadeIn(symbols[1], 0.5 * UP),
        )
        self.wait()
