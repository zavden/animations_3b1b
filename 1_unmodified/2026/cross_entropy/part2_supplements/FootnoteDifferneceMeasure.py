# ==============================================================================
# Scene:      FootnoteDifferneceMeasure
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 507-519)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FootnoteDifferneceMeasure.py FootnoteDifferneceMeasure -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FootnoteDifferneceMeasure(InteractiveScene):
    def construct(self):
        # Test
        footnote = TexText(R"""
            $^*$ The difference metric the authors defined is slightly \\
            more complicated. Define the expression above to be $\Delta_{Ab}$, \\
            for text $A$ and a small sample $b$ from text $B$. The full \\
            difference between documents was defined as
            $$S_{AB} := (\Delta_{Ab} - \Delta_{Bb}) / |b|$$
        """, alignment="")
        footnote[R"S_{AB} := (\Delta_{Ab} - \Delta_{Bb}) / |b|"].match_x(footnote).scale(1.5, about_edge=UP)
        footnote.scale(0.5)
        self.add(footnote)
