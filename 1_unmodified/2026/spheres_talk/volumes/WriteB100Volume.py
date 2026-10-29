# ==============================================================================
# Scene:      WriteB100Volume
# Source:     videos/_2026/spheres_talk/volumes.py (lines 1346-1350)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteB100Volume.py WriteB100Volume -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteB100Volume(InteractiveScene):
    def construct(self):
        # Test
        formula = Tex(R"B^{100} \rightarrow {\pi^{50} \over 50!} \approx 2.37 \times 10^{-40}")
        self.add(formula)
