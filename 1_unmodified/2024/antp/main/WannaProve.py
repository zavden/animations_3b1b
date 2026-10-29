# ==============================================================================
# Scene:      WannaProve
# Source:     videos/_2024/antp/main.py (lines 1079-1098)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WannaProve.py WannaProve -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WannaProve(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        morty = Mortimer()
        VGroup(randy, morty).to_edge(DOWN)
        randy.set_x(-3)
        morty.set_x(3)
        morty.make_eye_contact(randy)

        self.play(
            randy.says("Twin primes\nare infinite!", mode="hooray"),
            morty.change("concentrating")
        )
        self.wait()
        self.play(
            FadeOut(randy.bubble),
            randy.change("pondering", look_at=3 * UP),
            morty.change("raise_right_hand", look_at=3 * UP)
        )
