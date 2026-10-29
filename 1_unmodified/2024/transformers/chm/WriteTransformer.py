# ==============================================================================
# Scene:      WriteTransformer
# Source:     videos/_2024/transformers/chm.py (lines 251-255)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteTransformer.py WriteTransformer -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WriteTransformer(InteractiveScene):
    def construct(self):
        text = Text("Transformer", font_size=120)
        self.play(Write(text))
        self.wait()
