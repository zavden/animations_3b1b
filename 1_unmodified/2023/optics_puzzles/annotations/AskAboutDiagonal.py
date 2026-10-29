# ==============================================================================
# Scene:      AskAboutDiagonal
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 950-955)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutDiagonal.py AskAboutDiagonal -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutDiagonal(InteractiveScene):
    def construct(self):
        randy = Randolph(height=2)
        self.play(randy.says("Why diagonal?", mode="maybe", look_at=DOWN))
        self.play(Blink(randy))
        self.wait()
