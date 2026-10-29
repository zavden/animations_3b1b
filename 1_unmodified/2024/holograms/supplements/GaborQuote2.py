# ==============================================================================
# Scene:      GaborQuote2
# Source:     videos/_2024/holograms/supplements.py (lines 1435-1445)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GaborQuote2.py GaborQuote2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GaborQuote2(InteractiveScene):
    def construct(self):
        # Test
        quote = TexText(R"""
            ``In holography, nature\\
            is on the inventor's side''
        """, font_size=60, alignment="")
        quote.to_edge(RIGHT)

        self.play(Write(quote), run_time=2, lag_ratio=0.1)
        self.wait()
