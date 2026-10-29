# ==============================================================================
# Scene:      ThoughtBubble
# Source:     videos/_2024/antp/main.py (lines 193-198)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThoughtBubble.py ThoughtBubble -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThoughtBubble(InteractiveScene):
    def construct(self):
        randy = Randolph()
        randy.to_edge(LEFT)
        bubble = randy.get_bubble("Suppose\nnot...")
        self.add(bubble, bubble.content)
