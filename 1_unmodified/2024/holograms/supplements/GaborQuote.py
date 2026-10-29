# ==============================================================================
# Scene:      GaborQuote
# Source:     videos/_2024/holograms/supplements.py (lines 1418-1432)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GaborQuote.py GaborQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GaborQuote(InteractiveScene):
    def construct(self):
        # Test
        quote = TexText(R"""
            ``This was an exercise\\
            in serendipity, the art of\\
            looking for something and\\
            finding something else''
        """, font_size=60, alignment="")
        quote.to_edge(RIGHT)

        self.play(Write(quote), run_time=2, lag_ratio=0.01)
        self.play(quote["looking for something"].animate.set_color(BLUE), lag_ratio=0.1)
        self.play(quote["finding something else"].animate.set_color(TEAL), lag_ratio=0.1)
        self.wait()
