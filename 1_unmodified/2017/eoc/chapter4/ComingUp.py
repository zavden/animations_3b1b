# ==============================================================================
# Scene:      ComingUp
# Source:     videos/_2017/eoc/chapter4.py (lines 243-254)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComingUp.py ComingUp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComingUp(Scene):
    def construct(self):
        rect = Rectangle(height = 9, width = 16)
        rect.set_stroke(WHITE)
        rect.set_height(FRAME_HEIGHT-2)
        title = OldTexText("Coming up...")
        title.to_edge(UP)
        rect.next_to(title, DOWN)

        self.play(Write(title))
        self.play(ShowCreation(rect))
        self.wait()
