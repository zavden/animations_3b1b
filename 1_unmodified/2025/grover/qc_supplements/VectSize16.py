# ==============================================================================
# Scene:      VectSize16
# Source:     videos/_2025/grover/qc_supplements.py (lines 400-407)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VectSize16.py VectSize16 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VectSize16(InteractiveScene):
    def construct(self):
        # Test
        brace = Brace(Line(3 * DOWN, 3 * UP), RIGHT)
        tex = brace.get_tex("2^{4} = 16")
        tex.shift(SMALL_BUFF * UR)
        self.play(GrowFromCenter(brace), Write(tex))
        self.wait()
