# ==============================================================================
# Scene:      WriteGroversAlgorithm
# Source:     videos/_2025/grover/qc_supplements.py (lines 330-334)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteGroversAlgorithm.py WriteGroversAlgorithm -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteGroversAlgorithm(InteractiveScene):
    def construct(self):
        text = TexText("Grover's Algorithm", font_size=60)
        self.play(Write(text))
        self.wait()
