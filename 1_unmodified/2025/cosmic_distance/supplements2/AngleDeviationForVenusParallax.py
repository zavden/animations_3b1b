# ==============================================================================
# Scene:      AngleDeviationForVenusParallax
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 24-31)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AngleDeviationForVenusParallax.py AngleDeviationForVenusParallax -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AngleDeviationForVenusParallax(InteractiveScene):
    def construct(self):
        # Test
        title = TexText(R"Angle deviation $ = 2 \tan^{-1}(1 / 6200) \approx$ 1 arc-minute = $\displaystyle \frac{1}{60} \cdot 1^\circ$")
        title.to_edge(UP)

        self.play(Write(title))
        self.wait()
