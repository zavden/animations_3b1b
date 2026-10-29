# ==============================================================================
# Scene:      Equals2
# Source:     videos/_2018/cramer.py (lines 2181-2184)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Equals2.py Equals2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Equals2(Scene):
    def construct(self):
        self.add(OldTex("=2").add_background_rectangle())
        self.wait()
