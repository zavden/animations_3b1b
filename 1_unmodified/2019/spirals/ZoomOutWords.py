# ==============================================================================
# Scene:      ZoomOutWords
# Source:     videos/_2019/spirals.py (lines 2019-2024)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ZoomOutWords.py ZoomOutWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ZoomOutWords(Scene):
    def construct(self):
        words = OldTexText("Zoom out!")
        words.scale(3)
        self.play(FadeInFromLarge(words))
        self.wait()
