# ==============================================================================
# Scene:      Question3
# Source:     videos/_2018/sphere_area.py (lines 3380-3403)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Question3.py Question3 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Question3(Scene):
    def construct(self):
        question = OldTexText("Question \\#3:")
        question.to_edge(LEFT)
        equation = OldTexText(
            "(Shadow area)", "=", "$\\frac{1}{2}$",
            "(Area of one of the rings)"
        )
        equation[0][1:-1].set_color(YELLOW)
        equation[3][1:-1].set_color(PINK)
        equation.next_to(question, RIGHT)
        which_one = OldTexText("Which one?")
        # which_one.set_color(YELLOW)
        brace = Brace(equation[-1], DOWN, buff=SMALL_BUFF)
        which_one.next_to(brace, DOWN, SMALL_BUFF)

        self.add(question)
        self.play(FadeIn(equation))
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(which_one)
        )
        self.wait()
