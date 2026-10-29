# ==============================================================================
# Scene:      AskRecipriocalQuestion
# Source:     videos/_2017/eoc/chapter3.py (lines 1997-2007)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskRecipriocalQuestion.py AskRecipriocalQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskRecipriocalQuestion(Scene):
    def construct(self):
        tex = OldTex(
            "(\\text{What number?})",  
            "\\cdot x = 1"
        )
        arrow = Arrow(DOWN+LEFT, UP+RIGHT)
        arrow.move_to(tex[0].get_top(), DOWN+LEFT)
        self.play(Write(tex))
        self.play(ShowCreation(arrow))
        self.wait()
