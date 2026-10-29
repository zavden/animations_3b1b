# ==============================================================================
# Scene:      AskAboutUnsolved
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 570-576)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutUnsolved.py AskAboutUnsolved -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutUnsolved(InteractiveScene):
    def construct(self):
        randy = Randolph()
        randy.to_corner(DL)
        self.play(randy.says("What about the\nunsolved problem?", "maybe"))
        self.play(Blink(randy))
        self.wait(2)
