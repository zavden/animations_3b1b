# ==============================================================================
# Scene:      IntroduceTetrahedronFootnote
# Source:     videos/_2017/putnam.py (lines 226-234)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceTetrahedronFootnote.py IntroduceTetrahedronFootnote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceTetrahedronFootnote(Scene):
    def construct(self):
        words = OldTexText("""
            $^*$Chosen independently with a \\\\
            uniform distribution on the sphere.
        """)
        words.to_corner(UP+LEFT)
        self.add(words)
        self.wait(2)
