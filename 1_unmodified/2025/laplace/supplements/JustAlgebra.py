# ==============================================================================
# Scene:      JustAlgebra
# Source:     videos/_2025/laplace/supplements.py (lines 934-947)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl JustAlgebra.py JustAlgebra -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class JustAlgebra(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer(mode="tease")
        morty.body.insert_n_curves(100)
        self.play(morty.says("Just algebra!", mode="hooray", look_at=2 * UL))
        self.play(Blink(morty))
        self.wait()
        self.play(
            FadeOut(morty.bubble),
            morty.change("tease", look_at=2 * UL + UP)
        )
        self.play(Blink(morty))
        self.wait()
