# ==============================================================================
# Scene:      RantOpenAndClose
# Source:     videos/_2017/eoc/chapter7.py (lines 335-347)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RantOpenAndClose.py RantOpenAndClose -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class RantOpenAndClose(Scene):
    def construct(self):
        opening, closing = [
            OldTexText(
                start, "Rant on infinitesimals", "$>$",
                arg_separator = ""
            )
            for start in ("$<$", "$<$/")
        ]
        self.play(FadeIn(opening))
        self.wait(2)
        self.play(Transform(opening, closing))
        self.wait(2)
