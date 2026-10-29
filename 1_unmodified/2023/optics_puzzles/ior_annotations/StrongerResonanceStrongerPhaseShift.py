# ==============================================================================
# Scene:      StrongerResonanceStrongerPhaseShift
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1182-1186)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StrongerResonanceStrongerPhaseShift.py StrongerResonanceStrongerPhaseShift -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StrongerResonanceStrongerPhaseShift(InteractiveScene):
    def construct(self):
        words = TexText(R"Stronger resonance $\rightarrow$ Bigger phase kick", font_size=60)
        words.to_edge(UP)
        self.add(words)
