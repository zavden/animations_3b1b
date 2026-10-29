# ==============================================================================
# Scene:      Zoom100Label
# Source:     videos/_2019/diffyq/part4/staging.py (lines 27-32)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Zoom100Label.py Zoom100Label -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Zoom100Label(Scene):
    def construct(self):
        text = OldTexText("100x Zoom")
        text.scale(2)
        self.play(GrowFromCenter(text))
        self.wait()
