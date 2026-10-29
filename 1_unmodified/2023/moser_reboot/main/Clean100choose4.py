# ==============================================================================
# Scene:      Clean100choose4
# Source:     videos/_2023/moser_reboot/main.py (lines 625-631)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Clean100choose4.py Clean100choose4 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Clean100choose4(InteractiveScene):
    def construct(self):
        self.add(Tex(R"""
            {100 \choose 4}
            =\frac{100(100-1)(100-2)(100-3)}{1 \cdot 2 \cdot 3 \cdot 4}
            =3{,}921{,}225 \text { quadruplets }
        """).to_edge(UP))
