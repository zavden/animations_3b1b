# ==============================================================================
# Scene:      SimpleImplies
# Source:     videos/_2026/hairy_ball/supplements.py (lines 70-74)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleImplies.py SimpleImplies -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleImplies(InteractiveScene):
    def construct(self):
        arrow = Tex(R"\Rightarrow", font_size=120)
        self.play(Write(arrow))
        self.wait()
