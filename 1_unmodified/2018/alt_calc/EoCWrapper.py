# ==============================================================================
# Scene:      EoCWrapper
# Source:     videos/_2018/alt_calc.py (lines 1320-1324)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EoCWrapper.py EoCWrapper -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class EoCWrapper(Scene):
    def construct(self):
        title = Title("Essence of calculus")
        self.play(Write(title))
        self.wait()
