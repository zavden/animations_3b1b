# ==============================================================================
# Scene:      NightBeforeQuote
# Source:     videos/_2022/galois/art_supplements.py (lines 135-149)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NightBeforeQuote.py NightBeforeQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NightBeforeQuote(InteractiveScene):
    def construct(self):
        # Write
        quote = OldTexText("""
            ``You will publicly ask Jacobi\\\\
            or Gauss to give their opinion\\\\
            not on the truth but on the\\\\
            importance of the theorems.''
        """, alignment="")[0]

        quote.to_edge(RIGHT)
        self.play(FadeIn(quote, run_time=2, lag_ratio=0.025))
        self.wait()
        self.play(quote[33:-2].animate.set_color(YELLOW).set_anim_args(lag_ratio=0.5, run_time=3))
        self.wait(2)
