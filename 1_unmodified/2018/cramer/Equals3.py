# ==============================================================================
# Scene:      Equals3
# Source:     videos/_2018/cramer.py (lines 2187-2190)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Equals3.py Equals3 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Equals3(Scene):
    def construct(self):
        self.add(OldTex("=3").add_background_rectangle())
        self.wait()
