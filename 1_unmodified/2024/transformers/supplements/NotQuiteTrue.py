# ==============================================================================
# Scene:      NotQuiteTrue
# Source:     videos/_2024/transformers/supplements.py (lines 978-988)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NotQuiteTrue.py NotQuiteTrue -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class NotQuiteTrue(InteractiveScene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DR)
        self.play(
            morty.says("Actually, that's not\nquite true!"),
            run_time=1
        )
        for x in range(2):
            self.play(Blink(morty))
            self.wait()
