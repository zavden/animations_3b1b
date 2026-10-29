# ==============================================================================
# Scene:      SatisfyThisDisbelief
# Source:     videos/_2023/gauss_int/supplements.py (lines 209-252)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SatisfyThisDisbelief.py SatisfyThisDisbelief -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SatisfyThisDisbelief(InteractiveScene):
    def construct(self):
        # Words
        words = Text("""
            What explanation would
            satisfy their disbelief?
        """, alignment="LEFT")
        words.set_backstroke(width=3)
        words.to_corner(UR)
        arrow = Arrow(words.get_left(), 2 * LEFT + 2 * UP)

        pis = VGroup(
            Mortimer(),
            Randolph(color=BLUE_D).flip(),
            Randolph(color=BLUE_E).flip(),
            Randolph(color=BLUE_C).flip(),
        )
        pis.arrange_in_grid()
        pis.set_height(4)
        pis.to_corner(DR)

        self.add(pis)
        pis[0].change_mode("happy")
        self.play(LaggedStart(
            pis[0].change("raise_right_hand"),
            pis[1].change("pondering", look_at=arrow.get_end()),
            pis[2].change("pondering", look_at=arrow.get_end()),
            pis[3].change("pondering", look_at=arrow.get_end()),
            lag_ratio=0.5
        ))
        for x in range(2):
            self.play(Blink(random.choice(pis)))
            self.wait()

        self.play(
            FadeIn(words, lag_ratio=0.1),
            GrowArrow(arrow),
            pis[0].change("raise_left_hand", look_at=words),
            *(pi.animate.look_at(words) for pi in pis[1:])
        )
        for x in range(3):
            self.play(Blink(random.choice(pis)))
            self.wait()
        self.wait()
