# ==============================================================================
# Scene:      Footnote
# Source:     videos/_2017/eoc/footnote.py (lines 650-658)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Footnote.py Footnote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Footnote(Scene):
    def construct(self):
        self.add(OldTexText("""
            Interestingly, there is a notion in math 
            called the ``exterior derivative'' which 
            treats this ``d'' as having a more independent 
            meaning, though it's less related to the 
            intuitions I've introduced in this series.
        """, alignment = ""))
