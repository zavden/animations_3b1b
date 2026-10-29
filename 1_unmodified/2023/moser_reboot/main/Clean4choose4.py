# ==============================================================================
# Scene:      Clean4choose4
# Source:     videos/_2023/moser_reboot/main.py (lines 607-613)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Clean4choose4.py Clean4choose4 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Clean4choose4(InteractiveScene):
    def construct(self):
        self.add(Tex(R"""
            {4 \choose 4}
            =\frac{4(4-1)(4-2)(4-3)}{1 \cdot 2 \cdot 3 \cdot 4}
            =1 \text { quadruplet }
        """).to_edge(UP))
