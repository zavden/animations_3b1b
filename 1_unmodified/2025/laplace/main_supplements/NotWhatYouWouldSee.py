# ==============================================================================
# Scene:      NotWhatYouWouldSee
# Source:     videos/_2025/laplace/main_supplements.py (lines 720-731)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NotWhatYouWouldSee.py NotWhatYouWouldSee -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NotWhatYouWouldSee(InteractiveScene):
    def construct(self):
        morty = Mortimer().flip()
        morty.to_corner(DL)
        self.play(
            morty.says("Not the\nstandard form", mode="hesitant")
        )
        self.play(Blink(morty))
        self.wait()
        self.play(morty.debubble(mode="pondering", look_at=5 * UL))
        self.play(Blink(morty))
        self.wait()
