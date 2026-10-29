# ==============================================================================
# Scene:      MoreInAMoment
# Source:     videos/_2025/laplace/main_supplements.py (lines 202-209)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoreInAMoment.py MoreInAMoment -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoreInAMoment(InteractiveScene):
    def construct(self):
        morty = Mortimer()
        morty.body.insert_n_curves(1000)
        self.play(morty.says("Much, much more on\nthis in a moment"))
        self.play(morty.change("tease"))
        self.play(Blink(morty))
        self.wait()
