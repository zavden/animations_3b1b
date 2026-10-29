# ==============================================================================
# Scene:      SubtlePangolin
# Source:     videos/_2020/sir.py (lines 1874-1883)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SubtlePangolin.py SubtlePangolin -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SubtlePangolin(Scene):
    def construct(self):
        pangolin = SVGMobject(file_name="pangolin")
        pangolin.set_height(0.5)
        pangolin.set_fill(GREY_BROWN, opacity=0)
        pangolin.set_stroke(GREY_BROWN, width=1)
        self.play(ShowCreationThenFadeOut(pangolin))
        self.play(FadeOut(pangolin))

        self.embed()
