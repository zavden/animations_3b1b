# ==============================================================================
# Scene:      FiniteExpectations
# Source:     videos/_2023/clt/wordy_scenes.py (lines 1246-1249)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FiniteExpectations.py FiniteExpectations -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class FiniteExpectations(InteractiveScene):
    def construct(self):
        tex = TexText(R"And finite $E[X]$ for that matter", t2c={"X": BLUE})
        self.add(tex)
