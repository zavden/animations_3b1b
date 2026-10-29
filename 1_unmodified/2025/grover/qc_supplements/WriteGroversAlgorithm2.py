# ==============================================================================
# Scene:      WriteGroversAlgorithm2
# Source:     videos/_2025/grover/qc_supplements.py (lines 873-878)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteGroversAlgorithm2.py WriteGroversAlgorithm2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteGroversAlgorithm2(InteractiveScene):
    def construct(self):
        text = TexText("Grover's Algorithm", font_size=72)
        text.to_edge(UP)
        self.play(Write(text))
        self.wait()
