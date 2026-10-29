# ==============================================================================
# Scene:      DetailsNotDiscussed
# Source:     videos/_2024/transformers/supplements.py (lines 2124-2162)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DetailsNotDiscussed.py DetailsNotDiscussed -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DetailsNotDiscussed(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Details not discussed")
        title.add(Underline(title))
        title.scale(1.25)
        title.set_color(RED)
        title.to_edge(UP).to_edge(RIGHT, buff=0)

        details = VGroup(
            Text("Tokenization"),
            Text("Positional encoding"),
            Text("Layer normalization"),
            Text("Training"),
        )
        dots = Dot().get_grid(len(details), 1, buff=0.75)
        dots.next_to(title, DOWN, buff=MED_LARGE_BUFF).shift(2 * LEFT)
        for detail, dot in zip(details, dots):
            detail.next_to(dot, RIGHT)
            detail.add_to_back(dot)
        vdots = Tex(R"\vdots")
        vdots.next_to(details, DOWN, MED_LARGE_BUFF).shift(LEFT)
        details.add(vdots)
        details.set_color(GREY_A)

        self.add(title)
        self.play(
            LaggedStartMap(FadeIn, details, shift=0.25 * DOWN, lag_ratio=0.5),
            run_time=4
        )
        self.wait()

        # Highlight training
        self.play(
            details[-2][1:].animate.scale(2, about_edge=LEFT).set_color(WHITE),
            details[-1].animate.shift(0.1 * DOWN),
            details[:-2].animate.set_opacity(0.5).scale(0.9, about_edge=UL),
        )
        self.wait()
