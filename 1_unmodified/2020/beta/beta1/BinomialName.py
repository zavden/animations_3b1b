# ==============================================================================
# Scene:      BinomialName
# Source:     videos/_2020/beta/beta1.py (lines 946-953)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BinomialName.py BinomialName -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BinomialName(Scene):
    def construct(self):
        text = OldTexText("Probabilities of probabilities\\\\", "Part 1")
        text.set_width(FRAME_WIDTH - 1)
        text[0].set_color(BLUE)
        self.add(text[0])
        self.play(Write(text[1], run_time=2))
        self.wait(2)
