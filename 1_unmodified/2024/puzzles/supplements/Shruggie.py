# ==============================================================================
# Scene:      Shruggie
# Source:     videos/_2024/puzzles/supplements.py (lines 800-811)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Shruggie.py Shruggie -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Shruggie(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer(mode="shruggie").flip()
        self.add(morty)
        random.seed(1)
        for _ in range(10):
            x = random.random()
            if x < 0.25:
                self.play(Blink(morty))
            else:
                self.wait()
