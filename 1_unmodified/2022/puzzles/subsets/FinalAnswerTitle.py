# ==============================================================================
# Scene:      FinalAnswerTitle
# Source:     videos/_2022/puzzles/subsets.py (lines 4623-4626)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FinalAnswerTitle.py FinalAnswerTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FinalAnswerTitle(InteractiveScene):
    def construct(self):
        answer = Tex("\\frac{1}{5}\\big(2^{2{,}000} + 4 \\cdot 2^{400}\\big)")
        self.add(answer)
