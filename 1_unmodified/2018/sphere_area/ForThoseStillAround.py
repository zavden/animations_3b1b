# ==============================================================================
# Scene:      ForThoseStillAround
# Source:     videos/_2018/sphere_area.py (lines 3628-3639)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ForThoseStillAround.py ForThoseStillAround -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ForThoseStillAround(Scene):
    def construct(self):
        words = OldTexText("Still here?")
        words.scale(1.5)
        url = OldTexText("3blue1brown.com/store")
        # url.scale(1.5)
        url.to_edge(UP, buff=MED_SMALL_BUFF)

        self.play(Write(words))
        self.wait()
        self.play(ReplacementTransform(words, url))
        self.wait()
