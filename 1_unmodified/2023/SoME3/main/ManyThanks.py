# ==============================================================================
# Scene:      ManyThanks
# Source:     videos/_2023/SoME3/main.py (lines 407-416)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyThanks.py ManyThanks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ManyThanks(InteractiveScene):
    def construct(self):
        morty = Mortimer()
        words = Text("Many thanks are in order")
        words.next_to(morty, DOWN)

        self.add(morty, words)
        self.play(morty.change("gracious"))
        self.play(Blink(morty))
        self.wait()
