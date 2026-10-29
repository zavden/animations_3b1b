# ==============================================================================
# Scene:      NewIntroWords
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 23-41)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NewIntroWords.py NewIntroWords -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class NewIntroWords(InteractiveScene):
    def construct(self):
        kw = dict(font_size=66)
        words = VGroup(
            Text("Last chapter", **kw),
            Text("Convolution between two Gaussians", **kw),
            Text("Central Limit Theorem", **kw),
            Text("Today: A satisfying visual argument", **kw),
        )
        words.to_edge(UP, buff=MED_SMALL_BUFF)

        last_word = VMobject()
        for word in words:
            self.play(
                FadeOut(last_word, 0.5 * UP),
                FadeIn(word, 0.5 * UP),
            )
            self.wait()
            last_word = word
