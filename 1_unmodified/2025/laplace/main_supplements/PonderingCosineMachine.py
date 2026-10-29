# ==============================================================================
# Scene:      PonderingCosineMachine
# Source:     videos/_2025/laplace/main_supplements.py (lines 675-684)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PonderingCosineMachine.py PonderingCosineMachine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PonderingCosineMachine(InteractiveScene):
    def construct(self):
        morty = Mortimer(height=1.5)
        morty.flip()
        morty.to_corner(UL)

        for mode in ["tease", "pondering"]:
            self.play(morty.change(mode, look_at=ORIGIN))
            self.play(Blink(morty))
            self.wait(2)
