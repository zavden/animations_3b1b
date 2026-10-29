# ==============================================================================
# Scene:      FraudIsInfeasible
# Source:     videos/_2017/crypto.py (lines 2408-2419)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FraudIsInfeasible.py FraudIsInfeasible -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FraudIsInfeasible(Scene):
    def construct(self):
        words = OldTexText(
            "Fraud", "$\\Leftrightarrow$",
            "Computationally infeasible"
        )
        words.set_color_by_tex("Fraud", RED)
        words.to_edge(UP)
        self.play(FadeIn(words[0]))
        self.play(FadeIn(words[2]))
        self.play(Write(words[1]))
        self.wait()
