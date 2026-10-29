# ==============================================================================
# Scene:      ThatWeKnowOf
# Source:     videos/_2018/div_curl.py (lines 2565-2568)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThatWeKnowOf.py ThatWeKnowOf -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThatWeKnowOf(Scene):
    def construct(self):
        words = OldTexText("*That we know of!")
        self.add(words)
