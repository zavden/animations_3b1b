# ==============================================================================
# Scene:      OutstandingChannel
# Source:     videos/_2021/quick_eigen.py (lines 1341-1350)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OutstandingChannel.py OutstandingChannel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OutstandingChannel(Scene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DR)
        self.play(PiCreatureSays(
            morty, OldTexText("Outstanding\\\\channel"), target_mode="hooray",
            bubble_config={"height": 3, "width": 4}
        ))
        self.play(Blink(morty))
        self.wait()
