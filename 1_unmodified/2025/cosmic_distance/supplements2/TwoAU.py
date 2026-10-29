# ==============================================================================
# Scene:      TwoAU
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 331-344)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoAU.py TwoAU -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoAU(InteractiveScene):
    def construct(self):
        # Test
        braces = VGroup(
            Brace(Line(ORIGIN, 3 * RIGHT), UP),
            Brace(Line(3 * LEFT, ORIGIN), UP),
        )
        labels = VGroup(brace.get_text("A.U.") for brace in braces)

        self.play(
            LaggedStartMap(GrowFromCenter, braces, lag_ratio=0.5),
            LaggedStartMap(FadeIn, labels, shift=0.25 * UP, lag_ratio=0.5),
        )
        self.wait()
