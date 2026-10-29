# ==============================================================================
# Scene:      Thanks
# Source:     videos/_2021/siggraph.py (lines 234-239)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thanks.py Thanks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thanks(Scene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DR)
        self.play(PiCreatureSays(morty, OldTexText("Thanks"), target_mode="gracious"))
        morty.look_at(OUT)
