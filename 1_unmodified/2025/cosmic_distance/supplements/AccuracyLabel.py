# ==============================================================================
# Scene:      AccuracyLabel
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 696-701)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AccuracyLabel.py AccuracyLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AccuracyLabel(InteractiveScene):
    def construct(self):
        label = VGroup(
            TexText("Estimate: $R_E = ...$"),
            TexText("True value: $R_E = 6{,}378$ km"),
        )
