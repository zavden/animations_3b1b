# ==============================================================================
# Scene:      ProblemSolvingToRecreation
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 697-745)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProblemSolvingToRecreation.py ProblemSolvingToRecreation -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ProblemSolvingToRecreation(InteractiveScene):
    def construct(self):
        # Test
        words = VGroup(
            Text("Solving\nproblems"),
            Text("Helpful\nconstructs"),
            Text("Recreational\nmath"),
        )
        words.arrange(RIGHT, buff=2.5)
        words.set_y(-1.5)
        mind_bending = Text("(Sometimes Mind-bending)", font_size=24)
        mind_bending.next_to(words[1], DOWN)

        arrows = VGroup(
            Arrow(w1, w2, thickness=4, buff=0.45)
            for w1, w2 in zip(words, words[1:])
        )
        arrows.space_out_submobjects(1.1)

        self.play(FadeIn(words[0], lag_ratio=0.1))
        self.wait()
        self.play(
            FadeIn(words[1], lag_ratio=0.1),
            GrowArrow(arrows[0]),
        )
        self.wait()
        self.play(FadeIn(mind_bending, 0.25 * DOWN))
        self.wait()

        # Move mind-bending
        mb = mind_bending["Mind-bending"]
        helpful = words[1]["Helpful"]

        self.play(
            mb.animate.scale(2).move_to(helpful),
            FadeOut(helpful, 0.25 * UP),
            FadeOut(mind_bending["(Sometimes"][0]),
            FadeOut(mind_bending[")"][0]),
        )
        self.play(
            FadeIn(words[2], lag_ratio=0.1),
            GrowArrow(arrows[1]),
        )
        self.wait()
        self.play(
            words[0].animate.set_opacity(0.1),
            arrows[0].animate.set_opacity(0.1),
        )
        self.wait()
