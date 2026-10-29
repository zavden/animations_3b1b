# ==============================================================================
# Scene:      SimpleSampleValue
# Source:     videos/_2025/grover/qc_supplements.py (lines 476-480)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleSampleValue.py SimpleSampleValue -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleSampleValue(InteractiveScene):
    def construct(self):
        value = Tex(R"|0011\rangle", font_size=60)
        value.set_fill(border_width=2)
        self.add(value)
