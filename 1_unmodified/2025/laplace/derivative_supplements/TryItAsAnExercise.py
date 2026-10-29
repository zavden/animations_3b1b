# ==============================================================================
# Scene:      TryItAsAnExercise
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 333-339)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TryItAsAnExercise.py TryItAsAnExercise -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TryItAsAnExercise(InteractiveScene):
    def construct(self):
        morty = Mortimer()
        morty.body.insert_n_curves(500)
        self.play(morty.says("Try it as\nan exercise", mode="tease"))
        self.play(Blink(morty))
        self.wait()
