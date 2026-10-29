# ==============================================================================
# Scene:      WriteInRadians
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 100-108)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteInRadians.py WriteInRadians -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteInRadians(Scene):
    def construct(self):
        words = OldTexText("In radians")
        words.set_color(YELLOW)
        square = SurroundingRectangle(OldTex("\\theta"))
        square.next_to(words, UP)
        self.play(ShowCreation(square))
        self.play(Write(words), FadeOut(square))
        self.wait()
