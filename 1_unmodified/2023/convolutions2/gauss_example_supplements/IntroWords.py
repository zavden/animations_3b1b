# ==============================================================================
# Scene:      IntroWords
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 5-20)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroWords.py IntroWords -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class IntroWords(InteractiveScene):
    def construct(self):
        # Test
        title1 = Text("Last video", font_size=72)
        title1.to_edge(UP)
        title2 = Text("Today: An important example", font_size=72)
        title2.move_to(title1)
        VGroup(title1, title2).set_backstroke(width=3)

        self.play(Write(title1, run_time=1))
        self.wait()
        self.play(
            FadeOut(title1, 0.5 * UP),
            FadeIn(title2, 0.5 * UP),
        )
        self.wait()
