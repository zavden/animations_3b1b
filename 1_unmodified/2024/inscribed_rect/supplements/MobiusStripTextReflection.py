# ==============================================================================
# Scene:      MobiusStripTextReflection
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 556-567)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MobiusStripTextReflection.py MobiusStripTextReflection -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MobiusStripTextReflection(InteractiveScene):
    def construct(self):
        # Text
        text = Text("Möbius Strip", font_size=72)
        text.to_edge(LEFT)
        text.shift(UP)
        reflection = text.copy().flip(RIGHT)
        reflection.set_y(-text.get_y())
        self.add(text)
        self.wait()
        self.play(TransformFromCopy(text, reflection, run_time=3))
        self.wait()
