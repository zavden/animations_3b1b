# ==============================================================================
# Scene:      SupplementVideoWrapper
# Source:     videos/_2017/crypto.py (lines 1323-1332)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SupplementVideoWrapper.py SupplementVideoWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SupplementVideoWrapper(Scene):
    def construct(self):
        title = OldTexText("How secure is 256 bit security?")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height = 6)
        rect.next_to(title, DOWN)
        self.add(title)
        self.play(ShowCreation(rect))
        self.wait()
