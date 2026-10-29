# ==============================================================================
# Scene:      NoteTheConstantSlope
# Source:     videos/_2017/fractal_dimension.py (lines 2505-2510)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NoteTheConstantSlope.py NoteTheConstantSlope -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NoteTheConstantSlope(Scene):
    def construct(self):
        words = OldTexText("Note the \\\\ constant slope")
        words.set_color(YELLOW)
        self.play(Write(words))
        self.wait(2)
