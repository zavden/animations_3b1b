# ==============================================================================
# Scene:      GroversAlgorithmLabel
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 155-167)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GroversAlgorithmLabel.py GroversAlgorithmLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GroversAlgorithmLabel(InteractiveScene):
    def construct(self):
        labels = VGroup(
            TexText("Quantum Computing"),
            TexText("Grover's Algorithm"),
        )
        self.play(FadeIn(labels[0], 0.5 * UP))
        self.wait()
        self.play(
            labels[0].animate.shift(UP),
            FadeIn(labels[1], 0.5 * UP)
        )
        self.wait()
