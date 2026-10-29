# ==============================================================================
# Scene:      UnitRVector
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 373-378)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnitRVector.py UnitRVector -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class UnitRVector(InteractiveScene):
    def construct(self):
        text = TexText(R"Unit vector in \\ the direction of $\vec{r}$")
        text.set_fill(YELLOW)
        text.set_backstroke(BLACK, 10)
        self.add(text)
