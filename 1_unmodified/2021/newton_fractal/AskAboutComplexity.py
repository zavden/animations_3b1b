# ==============================================================================
# Scene:      AskAboutComplexity
# Source:     videos/_2021/newton_fractal.py (lines 313-326)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutComplexity.py AskAboutComplexity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutComplexity(Scene):
    def construct(self):
        self.add(FullScreenRectangle())

        question = Text("What does this complexity reflect?")
        question.set_width(FRAME_WIDTH - 2)
        question.to_edge(UP)
        self.add(question)

        screen = ScreenRectangle()
        screen.set_height(6.0)
        screen.set_fill(BLACK, 1)
        screen.next_to(question, DOWN)
        self.add(screen)
