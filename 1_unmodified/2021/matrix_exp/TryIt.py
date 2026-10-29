# ==============================================================================
# Scene:      TryIt
# Source:     videos/_2021/matrix_exp.py (lines 5864-5878)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TryIt.py TryIt -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TryIt(Scene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DR)

        self.add(morty)

        self.play(PiCreatureSays(morty, "Try it!", target_mode="surprised", run_time=1))
        self.play(Blink(morty))
        self.wait(2)

        self.remove(morty.bubble, morty.bubble.content)
        self.play(PiCreatureSays(morty, "Brace yourself now...", target_mode="hesitant"))
        morty.look(ORIGIN)
        self.wait(2)
