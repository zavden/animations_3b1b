# ==============================================================================
# Scene:      ThisIsStillWhiteLight
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 164-178)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisIsStillWhiteLight.py ThisIsStillWhiteLight -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThisIsStillWhiteLight(InteractiveScene):
    def construct(self):
        # Test
        words = Text("This is still white light", font_size=60)
        words.to_edge(UP)
        arrow = Arrow(
            words["This"].get_bottom(), LEFT + 0.5 * UP,
            stroke_color=WHITE, stroke_width=8,
        )

        self.play(
            Write(words, run_time=1),
            FadeIn(arrow, RIGHT, run_time=4.0, rate_func=rush_into),
        )
        self.wait()
