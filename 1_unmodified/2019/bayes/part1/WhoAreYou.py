# ==============================================================================
# Scene:      WhoAreYou
# Source:     videos/_2019/bayes/part1.py (lines 4407-4410)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhoAreYou.py WhoAreYou -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhoAreYou(Scene):
    def construct(self):
        words = OldTexText("Who are you?")
        self.add(words)
