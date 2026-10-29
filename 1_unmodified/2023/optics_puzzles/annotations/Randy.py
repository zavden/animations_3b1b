# ==============================================================================
# Scene:      Randy
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 1299-1301)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Randy.py Randy -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Randy(InteractiveScene):
    def construct(self):
        self.add(Randolph(mode="confused"))
