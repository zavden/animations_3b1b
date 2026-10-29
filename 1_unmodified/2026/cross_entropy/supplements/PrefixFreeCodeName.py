# ==============================================================================
# Scene:      PrefixFreeCodeName
# Source:     videos/_2026/cross_entropy/supplements.py (lines 691-706)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrefixFreeCodeName.py PrefixFreeCodeName -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PrefixFreeCodeName(InteractiveScene):
    def construct(self):
        # Test
        phrase = Text("Prefix-free code", font_size=90)
        phrase.to_edge(UP, buff=LARGE_BUFF)
        words = VGroup(phrase["Prefix"], phrase["-free"], phrase["code"])

        self.play(ShowIncreasingSubsets(words), run_time=2)
        self.wait()
        self.play(
            words[1][0].animate.space_out_submobjects(0.2, about_edge=DOWN).set_opacity(0),
            words[0::2].animate.arrange(RIGHT, buff=MED_SMALL_BUFF).move_to(words)
        )
        self.wait()
        self.play(FlashAround(VGroup(words[0], words[2]), time_width=1.5, run_time=2))
        self.wait()
