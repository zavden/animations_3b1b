# ==============================================================================
# Scene:      PDefectEqualsQmark
# Source:     videos/_2020/beta/beta3.py (lines 2005-2014)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PDefectEqualsQmark.py PDefectEqualsQmark -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PDefectEqualsQmark(Scene):
    def construct(self):
        label = OldTex(
            "P(\\text{Defect}) = ???",
            tex_to_color_map={
                "\\text{Defect}": RED,
            }
        )
        self.play(FadeIn(label, DOWN))
        self.wait()
