# ==============================================================================
# Scene:      PiGesturingAtEarlyView
# Source:     videos/_2024/transformers/supplements.py (lines 822-831)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiGesturingAtEarlyView.py PiGesturingAtEarlyView -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PiGesturingAtEarlyView(PiCreatureScene):
    def construct(self):
        morty = self.pi_creature.flip()
        morty.to_corner(DR)
        morty.shift(0.5 * LEFT)
        morty.set_color(GREY_BROWN)
        morty.body.insert_n_curves(100)
        for mode in ["raise_right_hand", "well", "gracious", "well", "tease"]:
            self.play(morty.change(mode, ORIGIN + 2 * random.random() * UP))
            self.wait(3)
