# ==============================================================================
# Scene:      PolesAtOmegaI
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 352-362)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PolesAtOmegaI.py PolesAtOmegaI -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PolesAtOmegaI(InteractiveScene):
    def construct(self):
        t2c = {"{s}": YELLOW, R"\omega": PINK}
        pole_words = VGroup(
            Tex(R"\text{Pole at } {s} = +\omega i", t2c=t2c),
            Tex(R"\text{Pole at } {s} = -\omega i", t2c=t2c),
        )
        pole_words.arrange(DOWN, aligned_edge=LEFT)
        for words in pole_words:
            self.play(Write(words))
            self.wait()
