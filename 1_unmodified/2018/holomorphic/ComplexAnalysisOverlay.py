# ==============================================================================
# Scene:      ComplexAnalysisOverlay
# Source:     videos/_2018/holomorphic.py (lines 4-11)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexAnalysisOverlay.py ComplexAnalysisOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexAnalysisOverlay(Scene):
    def construct(self):
        words = OldTexText("Complex analysis")
        words.scale(1.25)
        words.to_edge(UP)
        words.add_background_rectangle()
        self.add(words)
        self.wait()
