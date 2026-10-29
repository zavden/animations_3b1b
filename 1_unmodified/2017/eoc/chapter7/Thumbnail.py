# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2017/eoc/chapter7.py (lines 2923-2928)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class Thumbnail(Scene):
    def construct(self):
        lim = OldTex("\\lim", "_{h", "\\to 0}")
        lim.set_color_by_tex("h", GREEN)
        lim.set_height(5)
        self.add(lim)
