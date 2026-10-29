# ==============================================================================
# Scene:      WriteBasis
# Source:     videos/_2017/waves.py (lines 2009-2014)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteBasis.py WriteBasis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class WriteBasis(Scene):
    def construct(self):
        words = OldTexText("Choice of ``basis''")
        words.set_width(FRAME_WIDTH-1)
        self.play(Write(words))
        self.wait()
