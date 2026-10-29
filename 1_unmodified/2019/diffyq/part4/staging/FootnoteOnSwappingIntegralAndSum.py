# ==============================================================================
# Scene:      FootnoteOnSwappingIntegralAndSum
# Source:     videos/_2019/diffyq/part4/staging.py (lines 1735-1749)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FootnoteOnSwappingIntegralAndSum.py FootnoteOnSwappingIntegralAndSum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FootnoteOnSwappingIntegralAndSum(Scene):
    def construct(self):
        words = OldTexText(
            """
            Typically in math, you have to be more\\\\
            careful swapping the order of sums like\\\\
            this when infinities are involved. Again,\\\\
            such questions are what real analysis \\\\
            is built for.
            """,
            alignment=""
        )

        self.add(words)
        self.wait()
