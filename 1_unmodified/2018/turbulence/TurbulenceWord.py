# ==============================================================================
# Scene:      TurbulenceWord
# Source:     videos/_2018/turbulence.py (lines 1774-1776)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TurbulenceWord.py TurbulenceWord -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TurbulenceWord(Scene):
    def construct(self):
        self.add(OldTexText("Turbulence").scale(2))
