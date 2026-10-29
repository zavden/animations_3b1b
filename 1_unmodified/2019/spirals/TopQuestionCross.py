# ==============================================================================
# Scene:      TopQuestionCross
# Source:     videos/_2019/spirals.py (lines 1435-1443)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TopQuestionCross.py TopQuestionCross -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TopQuestionCross(Scene):
    def construct(self):
        top_q = OldTexText("Why do", " primes", " cause", " spirals", "?")
        top_q.scale(2)
        top_q.to_edge(UP)
        cross = Cross(top_q)

        self.play(ShowCreation(cross))
        self.wait()
