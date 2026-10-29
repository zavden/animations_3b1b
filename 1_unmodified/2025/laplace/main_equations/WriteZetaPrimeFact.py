# ==============================================================================
# Scene:      WriteZetaPrimeFact
# Source:     videos/_2025/laplace/main_equations.py (lines 1729-1746)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteZetaPrimeFact.py WriteZetaPrimeFact -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteZetaPrimeFact(InteractiveScene):
    def construct(self):
        # Test
        formula = Tex(
            R"\frac{\zeta'({s})}{\zeta({s})} = \sum_{spacer} \sum_{k=1}^\infty \frac{1}{k} \frac{1}{p^{s}}",
            t2c={"{s}": YELLOW}
        )
        spacer = formula["spacer"][0]
        p_prime = TexText("$p$ prime")
        p_prime.replace(spacer)
        p_prime.scale(0.8, about_edge=UP)
        formula.remove(*spacer)
        formula.add(*p_prime)
        formula.sort()

        formula.to_edge(UP, buff=MED_SMALL_BUFF)
        self.play(Write(formula))
        self.wait()
