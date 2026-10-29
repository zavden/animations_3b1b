# ==============================================================================
# Scene:      AltPauseAndPonder
# Source:     videos/_2021/newton_fractal.py (lines 1980-1996)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AltPauseAndPonder.py AltPauseAndPonder -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AltPauseAndPonder(Scene):
    def construct(self):
        morty = Mortimer(height=2)
        morty.flip().to_corner(DL)
        self.play(PiCreatureSays(
            morty, OldTexText("Pause and\\\\Ponder", font_size=36),
            target_mode="hooray",
            bubble_config={
                "height": 2,
                "width": 3,
            }
        ))
        self.play(Blink(morty))
        self.wait(2)
        self.play(morty.change("thinking"))
        self.play(Blink(morty))
        self.wait()
