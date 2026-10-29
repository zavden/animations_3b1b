# ==============================================================================
# Scene:      PatronWords
# Source:     videos/_2018/sphere_area.py (lines 3642-3647)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PatronWords.py PatronWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PatronWords(Scene):
    def construct(self):
        words = OldTexText("\\$2+ Patrons get \\\\ 50\\% off")
        words.to_corner(UL)
        words.set_color(RED)
        self.add(words)
