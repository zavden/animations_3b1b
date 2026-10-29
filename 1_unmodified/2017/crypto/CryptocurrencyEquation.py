# ==============================================================================
# Scene:      CryptocurrencyEquation
# Source:     videos/_2017/crypto.py (lines 247-260)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CryptocurrencyEquation.py CryptocurrencyEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CryptocurrencyEquation(Scene):
    def construct(self):
        parts = OldTexText(
            "Ledger", 
            "- Trust",
            "+ Cryptography",
            "= Cryptocurrency"
        )
        VGroup(*parts[-1][1:]).set_color(YELLOW)
        parts.set_width(FRAME_WIDTH - LARGE_BUFF)

        for part in parts:
            self.play(FadeIn(part))
            self.wait(2)
