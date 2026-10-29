# ==============================================================================
# Scene:      TechnicalNuances
# Source:     videos/_2019/diffyq/part4/staging.py (lines 1085-1120)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TechnicalNuances.py TechnicalNuances -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TechnicalNuances(Scene):
    def construct(self):
        title = OldTexText("Technical nuances not discussed")
        title.scale(1.5)
        title.set_color(YELLOW)
        line = DashedLine(title.get_left(), title.get_right())
        line.next_to(title, DOWN, SMALL_BUFF)
        line.set_stroke(GREY_B, 3)

        questions = VGroup(*map(TexText, [
            "Does the value at $0.5$ matter?",
            "What does it mean to solve a PDE with\\\\"
            "a discontinuous initial condition?",
            "Is the limit of a sequence of solutions\\\\"
            "also a solution?",
            "Do all functions have a Fourier series?",
        ]))

        self.play(
            Write(title),
            ShowCreation(line),
        )
        title.add(line)
        self.play(
            title.to_edge, UP,
        )

        last_question = VMobject()
        for question in questions:
            question.next_to(line, DOWN, MED_LARGE_BUFF)
            self.play(
                FadeInFromDown(question),
                FadeOut(last_question, UP)
            )
            self.wait(2)
            last_question = question
