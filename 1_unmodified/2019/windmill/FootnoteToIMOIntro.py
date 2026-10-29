# ==============================================================================
# Scene:      FootnoteToIMOIntro
# Source:     videos/_2019/windmill.py (lines 299-303)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FootnoteToIMOIntro.py FootnoteToIMOIntro -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FootnoteToIMOIntro(Scene):
    def construct(self):
        words = OldTexText("$^*$Based on data from 2019 test")
        self.play(FadeIn(words, UP))
        self.wait()
