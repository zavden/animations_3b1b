# ==============================================================================
# Scene:      LastWordsQuote
# Source:     videos/_2022/galois/art_supplements.py (lines 91-118)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LastWordsQuote.py LastWordsQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LastWordsQuote(InteractiveScene):
    def construct(self):
        # French quote
        fr_quote = Text(
            """
            Ne pleure pas, Alfred! J'ai besoin de
            tout mon courage pour mourir à vingt ans!
            """,
            alignment="LEFT",
            font="Better Grade",
            font_size=72
        )
        fr_quote.to_corner(UR)
        self.add(fr_quote)

        # Write english quote
        en_quote = Text(
            """
            Do not cry, Alfred! I
            need all my courage to die
            at twenty years of age!
            """,
            alignment="LEFT",
        )
        en_quote.match_width(fr_quote)
        en_quote.next_to(fr_quote, DOWN, buff=1)
        self.play(FadeIn(en_quote, lag_ratio=0.1, run_time=6))
        self.wait()
