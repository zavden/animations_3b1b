# ==============================================================================
# Scene:      TrustComputationalWorkSupplement
# Source:     videos/_2017/crypto.py (lines 2398-2406)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TrustComputationalWorkSupplement.py TrustComputationalWorkSupplement -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TrustComputationalWorkSupplement(Scene):
    def construct(self):
        words = OldTexText(
            "Main tool: ", "Cryptographic hash functions"
        )
        words[1].set_color(YELLOW)
        self.add(words[0])
        self.play(Write(words[1]))
        self.wait()
