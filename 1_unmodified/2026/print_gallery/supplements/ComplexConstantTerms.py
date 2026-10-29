# ==============================================================================
# Scene:      ComplexConstantTerms
# Source:     videos/_2026/print_gallery/supplements.py (lines 357-373)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexConstantTerms.py ComplexConstantTerms -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexConstantTerms(InteractiveScene):
    def construct(self):
        # Test
        kw = dict(t2c={"{c}": GREEN, "z": YELLOW})
        equations = VGroup(
            Tex(R"f(z) = {c} \cdot z", **kw),
            Tex(R"f(0) = {c} \cdot 0 = 0", **kw),
            Tex(R"f(1) = {c} \cdot 1 = {c}", **kw),
        )
        equations.arrange(RIGHT, buff=1.5)
        equations.to_edge(UP)

        self.add(equations[0])
        self.wait()
        for eq in equations[1:]:
            self.play(Write(eq))
            self.wait()
