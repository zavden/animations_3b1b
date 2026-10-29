# ==============================================================================
# Scene:      OnceACleverDiscovery
# Source:     videos/_2019/windmill.py (lines 3629-3645)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OnceACleverDiscovery.py OnceACleverDiscovery -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OnceACleverDiscovery(Scene):
    def construct(self):
        energy = OldTexText("energy")
        rect = SurroundingRectangle(energy)
        words = OldTexText("Once a clever discovery")
        vect = Vector(DR)
        vect.next_to(rect.get_top(), UL, SMALL_BUFF)
        words.next_to(vect.get_start(), UP)
        words.set_color(YELLOW)
        vect.set_color(YELLOW)

        self.play(
            ShowCreation(vect),
            ShowCreation(rect),
        )
        self.play(FadeInFromDown(words))
        self.wait()
