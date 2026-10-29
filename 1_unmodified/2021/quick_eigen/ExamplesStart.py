# ==============================================================================
# Scene:      ExamplesStart
# Source:     videos/_2021/quick_eigen.py (lines 268-275)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExamplesStart.py ExamplesStart -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExamplesStart(Scene):
    def construct(self):
        words = OldTexText("Examples start\\\\at", " 4:53")
        words.set_width(8)
        words[-1].set_color(YELLOW)
        self.play(Write(words, run_time=1))
        self.play(FlashAround(words[1], stroke_width=8))
        self.wait()
