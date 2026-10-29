# ==============================================================================
# Scene:      SimpleBubble
# Source:     videos/_2024/antp/main.py (lines 201-203)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleBubble.py SimpleBubble -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SimpleBubble(InteractiveScene):
    def construct(self):
        self.add(OldThoughtBubble())
