# ==============================================================================
# Scene:      UnorderedPair
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 440-444)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnorderedPair.py UnorderedPair -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class UnorderedPair(InteractiveScene):
    def construct(self):
        tex = TexText(R"Unordered pairs: $\{A, B\} = \{B, A\}$", font_size=60)
        tex.to_edge(UP)
        self.add(tex)
