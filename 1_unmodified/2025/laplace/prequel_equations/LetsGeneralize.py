# ==============================================================================
# Scene:      LetsGeneralize
# Source:     videos/_2025/laplace/prequel_equations.py (lines 1082-1090)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LetsGeneralize.py LetsGeneralize -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LetsGeneralize(InteractiveScene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DR)
        self.play(
            morty.says("Let’s\n  generalize!", mode="hooray")
        )
        self.play(Blink(morty))
        self.wait(3)
