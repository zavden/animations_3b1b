# ==============================================================================
# Scene:      PhaseFlowWords
# Source:     videos/_2018/div_curl.py (lines 3189-3194)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PhaseFlowWords.py PhaseFlowWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PhaseFlowWords(Scene):
    def construct(self):
        words = OldTexText("``Phase flow''")
        words.scale(2)
        self.play(Write(words))
        self.wait()
