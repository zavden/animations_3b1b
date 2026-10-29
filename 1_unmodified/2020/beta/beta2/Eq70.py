# ==============================================================================
# Scene:      Eq70
# Source:     videos/_2020/beta/beta2.py (lines 284-289)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Eq70.py Eq70 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Eq70(Scene):
    def construct(self):
        label = OldTex("=", "70", "\\%", "?")
        fix_percent(label.get_part_by_tex("\\%")[0])
        self.play(FadeIn(label))
        self.wait()
