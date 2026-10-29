# ==============================================================================
# Scene:      Timeline
# Source:     videos/_2026/cross_entropy/supplements.py (lines 178-205)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Timeline.py Timeline -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Timeline(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame

        btn = list(range(1900, 2030, 10))
        timeline = NumberLine(
            (1900, 2030, 1),
            width=20,
            big_tick_numbers=btn,
            tick_size=0.05,
            longer_tick_multiple=2,
        )
        timeline.add_numbers(btn, group_with_commas=False)

        tip = ArrowTip(angle=-90 * DEG)
        tip.set_color(TEAL)
        tip.set_height(0.2)
        tip.move_to(timeline.n2p(2026), DOWN)

        frame.set_height(6).move_to(timeline, RIGHT)

        self.add(timeline, tip)
        self.play(
            tip.animate.move_to(timeline.n2p(1948), DOWN),
            frame.animate.match_x(timeline.n2p(1970)).set_anim_args(time_span=(1, 5)),
            run_time=6,
        )
