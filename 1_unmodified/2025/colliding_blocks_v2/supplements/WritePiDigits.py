# ==============================================================================
# Scene:      WritePiDigits
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 222-226)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WritePiDigits.py WritePiDigits -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WritePiDigits(InteractiveScene):
    def construct(self):
        eq = Tex(R"\pi = 3.14159265358 \dots")
        self.play(FadeIn(eq, lag_ratio=0.25, run_time=4))
        self.wait()
