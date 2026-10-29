# ==============================================================================
# Scene:      WriteTwoTo256PossibleSignatures
# Source:     videos/_2017/crypto.py (lines 1313-1321)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteTwoTo256PossibleSignatures.py WriteTwoTo256PossibleSignatures -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteTwoTo256PossibleSignatures(Scene):
    def construct(self):
        words = OldTexText(
            "$2^{256}$", "possible\\\\", "signatures"
        )
        words.scale(2)
        words.set_color_by_tex("256", BLUE)
        self.play(Write(words))
        self.wait()
