# ==============================================================================
# Scene:      RealPartOfInsert
# Source:     videos/_2018/uncertainty.py (lines 1354-1360)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RealPartOfInsert.py RealPartOfInsert -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class RealPartOfInsert(Scene):
    def construct(self):
        words = OldTexText("(Real part of the)")
        words.set_color(RED)
        self.add(words)
        self.play(Write(words))
        self.wait(5)
