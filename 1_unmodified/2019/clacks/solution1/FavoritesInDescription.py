# ==============================================================================
# Scene:      FavoritesInDescription
# Source:     videos/_2019/clacks/solution1.py (lines 148-152)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FavoritesInDescription.py FavoritesInDescription -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FavoritesInDescription(Scene):
    def construct(self):
        words = OldTexText("(See the description for \\\\ some favorites)")
        words.scale(1.5)
        self.add(words)
