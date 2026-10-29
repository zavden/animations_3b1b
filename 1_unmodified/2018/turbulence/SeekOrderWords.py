# ==============================================================================
# Scene:      SeekOrderWords
# Source:     videos/_2018/turbulence.py (lines 649-654)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SeekOrderWords.py SeekOrderWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SeekOrderWords(Scene):
    def construct(self):
        words = OldTexText("Seek order amidst chaos")
        words.scale(1.5)
        self.play(Write(words))
        self.wait()
