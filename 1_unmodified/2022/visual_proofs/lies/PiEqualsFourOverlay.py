# ==============================================================================
# Scene:      PiEqualsFourOverlay
# Source:     videos/_2022/visual_proofs/lies.py (lines 407-413)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiEqualsFourOverlay.py PiEqualsFourOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiEqualsFourOverlay(InteractiveScene):
    def construct(self):
        words = OldTexText("Fine, as long as\\\\$\\pi = 4$")
        words.scale(2)
        words.set_color(RED)
        self.play(Write(words, stroke_color=WHITE))
        self.wait()
