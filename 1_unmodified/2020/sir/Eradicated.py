# ==============================================================================
# Scene:      Eradicated
# Source:     videos/_2020/sir.py (lines 2457-2461)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Eradicated.py Eradicated -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Eradicated(Scene):
    def construct(self):
        word = OldTexText("Eradicated")
        word.set_color(GREEN)
        self.add(word)
