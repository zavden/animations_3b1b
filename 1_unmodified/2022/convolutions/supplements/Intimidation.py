# ==============================================================================
# Scene:      Intimidation
# Source:     videos/_2022/convolutions/supplements.py (lines 95-114)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Intimidation.py Intimidation -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Intimidation(InteractiveScene):
    def construct(self):
        pis = VGroup(*(Randolph(color=color) for color in (BLUE_C, BLUE_E, BLUE_D)))
        pis.arrange(DOWN, buff=LARGE_BUFF)
        pis.set_height(FRAME_HEIGHT - 1)
        pis.move_to(FRAME_WIDTH * LEFT / 4)

        self.play(LaggedStart(*(
            pi.change("pondering", look_at=3 * UR)
            for pi in pis
        )))
        self.play(LaggedStart(*(Blink(pi) for pi in pis)))
        self.wait()
        self.play(LaggedStart(*(
            pi.change(mode, look_at=3 * UR)
            for pi, mode in zip(pis, ("horrified", "maybe", "pleading"))
        )))
        for x in range(2):
            self.play(Blink(random.choice(pis)))
            self.wait()
