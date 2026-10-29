# ==============================================================================
# Scene:      ThisIsLight
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 420-426)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisIsLight.py ThisIsLight -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThisIsLight(InteractiveScene):
    def construct(self):
        morty = Mortimer(height=1.5)
        morty.to_corner(DR)
        self.play(morty.says("This is light!", mode="surprised"))
        self.play(Blink(morty))
        self.wait()
