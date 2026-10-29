# ==============================================================================
# Scene:      KeyDefinitions
# Source:     videos/_2026/cross_entropy/supplements.py (lines 468-508)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KeyDefinitions.py KeyDefinitions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class KeyDefinitions(InteractiveScene):
    def construct(self):
        # Write terms
        terms = VGroup(
            Text("Information"),
            Text("Entropy"),
        )
        terms.scale(1.5)
        terms.to_edge(UP)

        for v, term in zip([LEFT, RIGHT], terms):
            term.shift(0.25 * FRAME_WIDTH * v)

        self.play(LaggedStartMap(Write, terms, lag_ratio=0.5))
        self.wait()

        # From insight
        bulbs = VGroup()
        arrows = VGroup()
        for term in terms:
            bulb = ThoughtBubble()
            bulb.remove(bulb.content)
            bulb.set_stroke(WHITE, 1.5)
            bulb.match_height(term)
            bulb.next_to(term[0], LEFT)
            arrow = Vector(RIGHT, thickness=4)
            arrow.set_color(WHITE)
            arrow.next_to(bulb, RIGHT)
            term.target = term.generate_target()
            term.target.scale(0.8)
            term.target.next_to(VGroup(arrow), RIGHT, MED_SMALL_BUFF, index_of_submobject_to_align=0)

            bulbs.add(bulb)
            arrows.add(arrow)

        self.play(
            LaggedStartMap(FadeIn, bulbs, scale=4, lag_ratio=0.5),
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.5),
            LaggedStartMap(MoveToTarget, terms, lag_ratio=0.5),
        )
        self.wait()
