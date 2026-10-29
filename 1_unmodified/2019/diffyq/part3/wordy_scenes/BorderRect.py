# ==============================================================================
# Scene:      BorderRect
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 171-176)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BorderRect.py BorderRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BorderRect(Scene):
    def construct(self):
        rect = FullScreenFadeRectangle()
        rect.set_stroke(WHITE, 3)
        rect.set_fill(opacity=0)
        self.add(rect)
