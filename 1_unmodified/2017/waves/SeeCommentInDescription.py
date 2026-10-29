# ==============================================================================
# Scene:      SeeCommentInDescription
# Source:     videos/_2017/waves.py (lines 2885-2896)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SeeCommentInDescription.py SeeCommentInDescription -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class SeeCommentInDescription(Scene):
    def construct(self):
        words = OldTexText("""
            \\begin{flushleft}
            $^*$See comment in the \\\\
            description on single-headed \\\\
            vs. double-headed arrows
            \\end{flushleft}
        """)
        words.set_width(FRAME_WIDTH - 1)
        words.to_corner(DOWN+LEFT)
        self.add(words)
