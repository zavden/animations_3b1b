# ==============================================================================
# Scene:      VariableSum
# Source:     videos/_2023/clt/wordy_scenes.py (lines 1192-1197)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VariableSum.py VariableSum -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class VariableSum(InteractiveScene):
    def construct(self):
        expr = Tex(R"X_1 + X_2 + \cdots + X_n")
        for c in "12n":
            expr["X_" + c].set_color(BLUE)
        self.add(expr)
