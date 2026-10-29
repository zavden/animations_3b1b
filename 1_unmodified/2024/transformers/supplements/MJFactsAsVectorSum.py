# ==============================================================================
# Scene:      MJFactsAsVectorSum
# Source:     videos/_2024/transformers/supplements.py (lines 1741-1770)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MJFactsAsVectorSum.py MJFactsAsVectorSum -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MJFactsAsVectorSum(InteractiveScene):
    def construct(self):
        # Test
        facts = VGroup(
            Tex(Rf"\overrightarrow{{\text{{{fact}}}}}")
            for fact in [
                "Basketball",
                "Chicago Bulls",
                "Number 23",
                "Born 1963",
            ]
        )
        facts.add(Tex(R"\vdots"))
        facts.arrange(DOWN, buff=0.75)
        colors = ["#F88158", "#CE1141", YELLOW, GREY, WHITE]
        for fact, color in zip(facts, colors):
            fact.set_color(color)

        plusses = Tex(R"+").replicate(len(facts) - 1)
        for f1, f2, plus in zip(facts, facts[1:], plusses):
            plus.move_to(midpoint(f1.get_bottom(), f2.get_top()))

        self.add(facts[0])
        for fact, plus in zip(facts[1:], plusses):
            self.play(
                FadeIn(fact, shift=0.5 * DOWN),
                Write(plus),
                run_time=1,
            )
            self.wait()
