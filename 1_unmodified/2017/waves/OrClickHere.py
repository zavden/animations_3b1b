# ==============================================================================
# Scene:      OrClickHere
# Source:     videos/_2017/waves.py (lines 4195-4210)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OrClickHere.py OrClickHere -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class OrClickHere(Scene):
    def construct(self):
        words = OldTexText("Or click here")
        words.scale(3)
        arrow = Vector(
            2*UP + 2*RIGHT,
            rectangular_stem_width = 0.1,
            tip_length = 0.5
        )
        arrow.next_to(words, UP).shift(RIGHT)

        self.play(
            Write(words),
            ShowCreation(arrow)
        )
        self.wait()
