# ==============================================================================
# Scene:      WritePythagoreanTriple
# Source:     videos/_2017/triples.py (lines 178-184)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WritePythagoreanTriple.py WritePythagoreanTriple -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WritePythagoreanTriple(Scene):
    def construct(self):
        words = OldTexText("``Pythagorean triple''")
        words.set_width(FRAME_WIDTH - LARGE_BUFF)
        words.to_corner(DOWN+LEFT)
        self.play(Write(words))
        self.wait(2)
