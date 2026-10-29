# ==============================================================================
# Scene:      Thanks
# Source:     videos/_2021/newton_fractal.py (lines 4577-4589)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thanks.py Thanks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thanks(Scene):
    def construct(self):
        morty = Mortimer(mode="happy")
        thanks = Text("Thank you")
        thanks.next_to(morty, LEFT)
        self.play(
            morty.change("gracious"),
            FadeIn(thanks, lag_ratio=0.1)
        )
        for n in range(5):
            self.play(morty.animate.look([DL, DR][n % 2]))
            self.wait(random.random() * 5)
            self.play(Blink(morty))
