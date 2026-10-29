# ==============================================================================
# Scene:      Antidisk
# Source:     videos/_2025/cosmic_distance/part2.py (lines 295-303)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Antidisk.py Antidisk -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Antidisk(InteractiveScene):
    def construct(self):
        # Test
        rect = FullScreenRectangle()
        disk = Dot(radius=3)
        rect = Exclusion(rect, disk)
        rect.set_fill(GREEN_SCREEN, 1)
        rect.set_stroke(width=0)
        self.add(rect)
