# ==============================================================================
# Scene:      CircumferenceText
# Source:     videos/_2018/basel/basel2.py (lines 3751-3757)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CircumferenceText.py CircumferenceText -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class CircumferenceText(Scene):
    CONFIG = {"n" : 16}
    def construct(self):
        words = OldTexText("Circumference %d"%self.n)
        words.scale(1.25)
        words.to_corner(UP+LEFT)
        self.add(words)
