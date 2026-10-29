# ==============================================================================
# Scene:      CompareLightSpeedEstimates
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 378-389)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareLightSpeedEstimates.py CompareLightSpeedEstimates -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompareLightSpeedEstimates(InteractiveScene):
    def construct(self):
        # Test
        words = VGroup(
            TexText("Huygens' Estimate: 212,000 km/s"),
            TexText("True speed: 299,792 km/s"),
        )
        words.arrange(DOWN, aligned_edge=RIGHT)
        words.to_corner(UL)
        for word in words:
            self.play(Write(word))
            self.wait()
