# ==============================================================================
# Scene:      LookAtScrolling
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 216-238)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LookAtScrolling.py LookAtScrolling -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LookAtScrolling(InteractiveScene):
    random_seed = 1

    def construct(self):
        morty = Mortimer()
        morty.set_height(3)
        morty.to_edge(RIGHT)

        self.play(morty.change("pondering", 3 * DOWN))
        for _ in range(4):
            self.play(morty.change(
                random.choice(["tease", "pondering"]),
                3 * UP
            ))
            if random.random() < 0.3:
                self.play(Blink(morty))
            else:
                self.wait()
            self.play(morty.animate.look_at(3 * DOWN))
            if random.random() < 0.3:
                self.play(Blink(morty))
            else:
                self.wait()
