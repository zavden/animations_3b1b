# ==============================================================================
# Scene:      FirstStepIsToCare
# Source:     videos/_2021/siggraph.py (lines 215-219)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FirstStepIsToCare.py FirstStepIsToCare -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FirstStepIsToCare(Scene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DR)
        self.play(PiCreatureSays(morty, OldTexText("The first step\\\\is to care.")))
