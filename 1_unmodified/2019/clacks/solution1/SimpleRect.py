# ==============================================================================
# Scene:      SimpleRect
# Source:     videos/_2019/clacks/solution1.py (lines 1111-1113)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleRect.py SimpleRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleRect(Scene):
    def construct(self):
        self.add(Rectangle(width=6, height=2, color=WHITE))
