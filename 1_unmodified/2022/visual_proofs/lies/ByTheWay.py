# ==============================================================================
# Scene:      ByTheWay
# Source:     videos/_2022/visual_proofs/lies.py (lines 2358-2361)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ByTheWay.py ByTheWay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ByTheWay(InteractiveScene):
    def construct(self):
        self.play(Write(Text("By the way...")))
        self.wait()
