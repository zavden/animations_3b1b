# ==============================================================================
# Scene:      Footnote
# Source:     videos/_2017/waves.py (lines 4274-4294)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Footnote.py Footnote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class Footnote(Scene):
    def construct(self):
        words = OldTexText("""
            \\begin{flushleft}
            \\Large
            By the way, in the quantum mechanical description
            of polarization, states are written like 
            $|\\! \\leftrightarrow \\rangle$ with a double-headed
            arrow, rather than $|\\! \\rightarrow \\rangle$ with
            a single-headed arrow.  This conveys how there's no distinction
            between left and right; they each have the same measurable 
            state: horizontal. \\\\
            \\quad \\\\
            Because of how I chose to motivate things with classical waves,
            I'll stick with the single-headed $|\\! \\rightarrow \\rangle$
            for this video, but just keep in mind that this differs
            from quantum mechanics conventions.
            \\end{flushleft}
        """)
        words.set_width(FRAME_WIDTH - 2)
        self.add(words)
