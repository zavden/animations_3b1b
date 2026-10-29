# ==============================================================================
# Scene:      FromBracketFootnote
# Source:     videos/_2017/waves.py (lines 1886-1894)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FromBracketFootnote.py FromBracketFootnote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class FromBracketFootnote(Scene):
    def construct(self):
        words = OldTexText(
            "From, ``Bra", "ket", "''",
            arg_separator = ""
        )
        words.set_color_by_tex("ket", YELLOW)
        words.set_width(FRAME_WIDTH - 1)
        self.add(words)
