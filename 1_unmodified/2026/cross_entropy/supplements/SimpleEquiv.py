# ==============================================================================
# Scene:      SimpleEquiv
# Source:     videos/_2026/cross_entropy/supplements.py (lines 299-302)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleEquiv.py SimpleEquiv -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SimpleEquiv(InteractiveScene):
    def construct(self):
        self.play(Write(Tex(R"\Leftrightarrow", font_size=90)))
        self.wait()
