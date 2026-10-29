# ==============================================================================
# Scene:      ShowGradientEquation
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 475-504)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowGradientEquation.py ShowGradientEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowGradientEquation(InteractiveScene):
    def construct(self):
        # Test
        kw = dict(t2c={"q": PINK, "q_i": PINK, "p_i": GREEN, R"\lambda": BLUE})
        equations = VGroup(
            Tex(R"\nabla_q \left(\sum_i p_i f(q_i) \right) = \lambda \nabla_q \left(\sum_i q_i \right)", **kw),
            Tex(R"p_i f'(q_i) = \lambda", **kw),
            Tex(R"q_i f'(q_i) = \lambda", **kw),
            Tex(R"f'(q) = {\lambda \over q}", **kw),
        )
        equations.arrange(DOWN, buff=MED_LARGE_BUFF)
        equations[1:].shift(LEFT)
        annotations = VGroup(
            TexText("for all $i$"),
            TexText(R"Assuming minimum $\Leftrightarrow q_i = p_i$", **kw),
            Tex(R"f(q) = \lambda \log(q)", **kw),
        )
        for annotation, equation in zip(annotations, equations[1:]):
            arrow = Vector(0.75 * LEFT).next_to(equation, RIGHT)
            if equation is equations[-1]:
                arrow.flip()
            annotation.scale(0.8)
            annotation.next_to(arrow, RIGHT)
            annotation.add_to_back(arrow)
            equation.add(annotation)

        self.play(FadeIn(equations[0], DOWN))
        self.wait()
        self.play(LaggedStartMap(FadeIn, equations[1:], shift=DOWN, lag_ratio=0.25))
        self.wait(4)
