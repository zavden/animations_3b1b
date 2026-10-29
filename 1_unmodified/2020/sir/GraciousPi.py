# ==============================================================================
# Scene:      GraciousPi
# Source:     videos/_2020/sir.py (lines 3102-3114)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GraciousPi.py GraciousPi -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GraciousPi(Scene):
    def construct(self):
        morty = Mortimer()
        morty.flip()
        self.play(FadeIn(morty))
        self.play(morty.change, "hesitant")
        self.play(Blink(morty))
        self.wait()
        self.play(morty.change, "gracious", morty.get_bottom())
        self.play(Blink(morty))
        self.wait(2)
        self.play(Blink(morty))
        self.wait(2)
