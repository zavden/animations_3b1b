# ==============================================================================
# Scene:      SeeCommentInDescriptionAgain
# Source:     videos/_2017/waves.py (lines 2898-2903)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SeeCommentInDescriptionAgain.py SeeCommentInDescriptionAgain -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class SeeCommentInDescriptionAgain(Scene):
    def construct(self):
        words = OldTexText("$^*$Again, see description")
        words.set_width(FRAME_WIDTH - 1)
        words.to_corner(DOWN+LEFT)
        self.add(words)
