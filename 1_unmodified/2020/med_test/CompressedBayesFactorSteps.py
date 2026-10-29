# ==============================================================================
# Scene:      CompressedBayesFactorSteps
# Source:     videos/_2020/med_test.py (lines 5773-5786)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompressedBayesFactorSteps.py CompressedBayesFactorSteps -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompressedBayesFactorSteps(Scene):
    def construct(self):
        steps = OldTexText(
            "Step 1) ", "Express the prior with odds\\\\",
            "Step 2) ", "Compute the Bayes factor\\\\",
            "Step 3) ", "Multiply\\\\",
            alignment="",
        )
        steps[1].set_color(YELLOW)
        steps[3].set_color(GREEN)
        steps[5].set_color(BLUE)
        steps.set_width(FRAME_WIDTH - 2)

        self.add(steps)
