# ==============================================================================
# Scene:      Six
# Source:     videos/_2018/wallis.py (lines 390-396)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Six.py Six -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Six(Scene):
    def construct(self):
        six = OldTex("6")
        six.add_background_rectangle(opacity = 1)
        six.background_rectangle.stretch(1.5, 0)
        six.set_height(7)
        self.add(six)
