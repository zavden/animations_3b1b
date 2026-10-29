# ==============================================================================
# Scene:      GaussianQuestion
# Source:     videos/_2023/gauss_int/supplements.py (lines 798-823)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GaussianQuestion.py GaussianQuestion -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GaussianQuestion(InteractiveScene):
    def construct(self):
        # Test
        curve = FunctionGraph(lambda x: math.exp(-x**2), x_range=(-3, 3, 0.1))
        curve.set_width(6)
        curve.set_height(2, stretch=True)
        curve.to_edge(RIGHT).shift(UP)
        curve.set_stroke(BLUE, 3)

        func = Tex(R"{1 \over \sqrt{2 \pi} } e^{-x^2 / 2}", font_size=40)
        func.move_to(curve.get_bottom())

        question = Text("Where does this\ncome from?")
        question.next_to(func, DOWN, MED_LARGE_BUFF)

        year = Text("(1850)", font_size=40)
        year.next_to(question, DOWN, MED_LARGE_BUFF)
        year.set_fill(GREY_B)

        self.play(
            ShowCreation(curve),
            FadeIn(func),
            Write(question)
        )
        self.play(FadeIn(year, DOWN))
        self.wait(2)
