# ==============================================================================
# Scene:      TwentyBitOverlay
# Source:     videos/_2022/wordle/scenes.py (lines 2193-2198)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwentyBitOverlay.py TwentyBitOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwentyBitOverlay(Scene):
    def construct(self):
        eq = OldTex("20 \\text{ bits} \\Leftrightarrow 0.00000095")
        eq.scale(1.5)
        self.play(Write(eq))
        self.wait()
