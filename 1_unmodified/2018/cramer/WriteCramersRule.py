# ==============================================================================
# Scene:      WriteCramersRule
# Source:     videos/_2018/cramer.py (lines 2116-2122)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteCramersRule.py WriteCramersRule -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteCramersRule(Scene):
    def construct(self):
        words = OldTexText("``Cramer's Rule''")
        words.set_width(FRAME_WIDTH - LARGE_BUFF)
        words.add_background_rectangle()
        self.play(Write(words))
        self.wait()
