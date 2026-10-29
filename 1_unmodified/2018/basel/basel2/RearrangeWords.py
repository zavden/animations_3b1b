# ==============================================================================
# Scene:      RearrangeWords
# Source:     videos/_2018/basel/basel2.py (lines 1142-1146)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RearrangeWords.py RearrangeWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class RearrangeWords(Scene):
    def construct(self):
        words = OldTexText("Rearrange without changing \\\\ the apparent brightness")
        self.play(Write(words))
        self.wait(5)
