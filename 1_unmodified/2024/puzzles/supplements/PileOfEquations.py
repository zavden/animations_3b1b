# ==============================================================================
# Scene:      PileOfEquations
# Source:     videos/_2024/puzzles/supplements.py (lines 915-930)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PileOfEquations.py PileOfEquations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PileOfEquations(InteractiveScene):
    def construct(self):
        # Test
        equations = VGroup(
            Tex(R"\mathbf{x} = \big\{(x_1, x_2, \ldots, x_8) \quad | x_i \in \mathbb{Z} \text{ or } x_i \in \mathbb{Z} + \frac{1}{2}\big\}"),
            Tex(R"\Delta(\Lambda) = \frac{V_n}{\det(\Lambda)}"),
            Tex(R"V_n = \frac{\pi^{n/2} r^n}{\Gamma(n/2 + 1)} \rightarrow V_8 = \frac{\pi^4}{24}"),
            Tex(R"\theta_{E_8}(z) = \sum_{\mathbf{x} \in E_8} e^{\pi i z |\mathbf{x}|^2}"),
            Tex(R"|\text{Aut}(E_8)| = 696,729,600 = 2^{14} \cdot 3^5 \cdot 5^2 \cdot 7"),
            Tex(R"\Delta_{\text{max}} \leq \frac{\pi^4}{384} + \epsilon"),
            Tex(R"\Delta \leq \frac{2^{-n}n}{e} \cdot \frac{\text{Vol}(B^n_1)}{\text{Vol}(V)}"),
        )
        equations.arrange(DOWN, aligned_edge=LEFT)
        equations.set_height(FRAME_HEIGHT - 1)
        self.play(LaggedStartMap(Write, equations, lag_ratio=0.5, run_time=7))
        self.wait()
