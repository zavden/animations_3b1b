# ==============================================================================
# Scene:      WeCanDoBetter
# Source:     videos/_2022/wordle/footnote.py (lines 789-799)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WeCanDoBetter.py WeCanDoBetter -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WeCanDoBetter(Scene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DR)
        self.play(PiCreatureSays(
            morty, OldTexText("We can do\\\\better!"),
            bubble_config=dict(width=3.5, height=2.5, fill_opacity=0.95),
        ))
        for x in range(2):
            self.play(Blink(morty))
            self.wait(2)
