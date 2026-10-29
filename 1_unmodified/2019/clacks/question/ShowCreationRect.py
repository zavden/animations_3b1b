# ==============================================================================
# Scene:      ShowCreationRect
# Source:     videos/_2019/clacks/question.py (lines 709-714)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowCreationRect.py ShowCreationRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowCreationRect(Scene):
    def construct(self):
        rect = SurroundingRectangle(OldTexText("\\# Collisions: 3"))
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.wait()
