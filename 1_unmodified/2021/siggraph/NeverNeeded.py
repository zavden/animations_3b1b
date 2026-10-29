# ==============================================================================
# Scene:      NeverNeeded
# Source:     videos/_2021/siggraph.py (lines 222-231)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NeverNeeded.py NeverNeeded -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NeverNeeded(Scene):
    def construct(self):
        formula = OldTex("\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}")
        formula.set_height(2)
        formula.to_corner(UL)
        self.add(formula)

        morty = Mortimer()
        morty.to_corner(DR)
        self.play(PiCreatureSays(morty, OldTexText("Who actually\\\\uses it!"), target_mode="angry"))
