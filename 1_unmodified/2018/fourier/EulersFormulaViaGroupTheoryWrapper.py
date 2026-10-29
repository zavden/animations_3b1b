# ==============================================================================
# Scene:      EulersFormulaViaGroupTheoryWrapper
# Source:     videos/_2018/fourier.py (lines 3150-3158)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EulersFormulaViaGroupTheoryWrapper.py EulersFormulaViaGroupTheoryWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EulersFormulaViaGroupTheoryWrapper(Scene):
    def construct(self):
        title = OldTexText("Euler's formula with introductory group theory")
        title.to_edge(UP)
        screen_rect = ScreenRectangle(height = 6)
        screen_rect.next_to(title, DOWN)
        self.add(title)
        self.play(ShowCreation(screen_rect))
        self.wait(2)
