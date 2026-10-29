# ==============================================================================
# Scene:      ThoughtBubbleWithLanguageQuestions
# Source:     videos/_2026/cross_entropy/supplements.py (lines 947-971)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThoughtBubbleWithLanguageQuestions.py ThoughtBubbleWithLanguageQuestions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThoughtBubbleWithLanguageQuestions(InteractiveScene):
    def construct(self):
        # Test
        contents = VGroup(
            Text("British vs.\nAmerican?"),
            Text("Slang?"),
            Text("Australian?"),
            Text("Jargon?"),
        )
        bubble = ThoughtBubble(contents)
        bubble.remove(contents)
        bubble[0][:3].flip(UR).next_to(bubble[0][3], LEFT).shift(0.5 * DOWN) 

        self.play(
            Write(bubble, run_time=2),
            FadeIn(contents[0], lag_ratio=0.1, time_span=(0.5, 2))
        )
        self.wait()
        for old, new in zip(contents, contents[1:]):
            self.play(LaggedStart(
                FadeIn(new, shift=0.2 * UP),
                FadeOut(old, shift=0.2 * UP),
                lag_ratio=0.3
            ))
            self.wait()
