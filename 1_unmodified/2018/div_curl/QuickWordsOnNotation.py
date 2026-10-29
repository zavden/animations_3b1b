# ==============================================================================
# Scene:      QuickWordsOnNotation
# Source:     videos/_2018/div_curl.py (lines 3289-3294)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuickWordsOnNotation.py QuickWordsOnNotation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuickWordsOnNotation(Scene):
    def construct(self):
        words = OldTexText("Quick words on notation:")
        words.scale(1.5)
        self.play(FadeInFromDown(words))
        self.wait()
