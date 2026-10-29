# ==============================================================================
# Scene:      Clean6choose4
# Source:     videos/_2023/moser_reboot/main.py (lines 616-622)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Clean6choose4.py Clean6choose4 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Clean6choose4(InteractiveScene):
    def construct(self):
        self.add(Tex(R"""
            {6 \choose 4}
            =\frac{6(6-1)(6-2)(6-3)}{1 \cdot 2 \cdot 3 \cdot 4}
            =15 \text { quadruplets }
        """).to_edge(UP))
