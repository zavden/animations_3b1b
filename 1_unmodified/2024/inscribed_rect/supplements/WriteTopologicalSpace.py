# ==============================================================================
# Scene:      WriteTopologicalSpace
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 748-754)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteTopologicalSpace.py WriteTopologicalSpace -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WriteTopologicalSpace(InteractiveScene):
    def construct(self):
        # Test
        text = Text("Topological Space", font_size=72)
        text.to_edge(UP)
        self.play(Write(text))
        self.wait()
