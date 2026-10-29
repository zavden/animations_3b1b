# ==============================================================================
# Scene:      TriPanelWithPi
# Source:     videos/_2024/transformers/supplements.py (lines 2165-2190)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TriPanelWithPi.py TriPanelWithPi -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class TriPanelWithPi(InteractiveScene):
    def construct(self):
        vlines = Line(UP, DOWN).replicate(2)
        vlines.set_height(FRAME_HEIGHT / 2)
        vlines.arrange(RIGHT, buff=FRAME_WIDTH / 3)
        vlines.to_edge(UP, buff=0)
        hline = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        hline.move_to(vlines, DOWN)
        lines = VGroup(*vlines, hline)

        lines.set_stroke(WHITE, 2)
        self.add(lines)

        # Test
        morty = Mortimer(mode="happy")
        morty.to_corner(DR).shift(3 * LEFT)

        self.play(morty.change("tease", 4 * UL))
        self.play(Blink(morty))
        self.wait()
        self.play(morty.change("coin_flip_2", 3 * UP))
        self.play(Blink(morty))
        self.wait()
        self.play(morty.change("hooray", 5 * UR).set_anim_args(path_arc=10 * DEGREES))
        self.play(Blink(morty))
        self.wait()
