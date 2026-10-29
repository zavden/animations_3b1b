# ==============================================================================
# Scene:      ByLine
# Source:     videos/_2018/wallis.py (lines 5040-5047)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ByLine.py ByLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ByLine(Scene):
    def construct(self):
        self.add(OldTexText("""
            Written and animated by \\\\
            \\quad \\\\
            Sridhar Ramesh \\\\
            Grant Sanderson
        """).shift(2 * UP))
