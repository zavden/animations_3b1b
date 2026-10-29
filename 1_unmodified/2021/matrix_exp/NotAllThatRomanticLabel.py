# ==============================================================================
# Scene:      NotAllThatRomanticLabel
# Source:     videos/_2021/matrix_exp.py (lines 5586-5596)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NotAllThatRomanticLabel.py NotAllThatRomanticLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NotAllThatRomanticLabel(Scene):
    def construct(self):
        text = OldTexText("Not all that\n\n romantic!")
        arrow = Vector(LEFT)
        arrow.next_to(text, LEFT)
        text.set_color(RED)
        arrow.set_color(RED)

        self.add(text)
        self.play(ShowCreation(arrow))
        self.wait()
