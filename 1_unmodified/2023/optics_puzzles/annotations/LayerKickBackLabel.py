# ==============================================================================
# Scene:      LayerKickBackLabel
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 1054-1059)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LayerKickBackLabel.py LayerKickBackLabel -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LayerKickBackLabel(InteractiveScene):
    def construct(self):
        layer_label = Text("Each layer kicks back the phase")
        layer_label.to_edge(UP)
        self.play(Write(layer_label))
        self.wait()
