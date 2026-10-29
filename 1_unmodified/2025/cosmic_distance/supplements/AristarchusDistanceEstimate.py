# ==============================================================================
# Scene:      AristarchusDistanceEstimate
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 960-975)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AristarchusDistanceEstimate.py AristarchusDistanceEstimate -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AristarchusDistanceEstimate(InteractiveScene):
    def construct(self):
        # Test
        t2c = {"D_S": YELLOW, "D_M": GREY_B}
        guess = TexText("Aristarchus's Guess: $D_S = 20 D_M$", t2c=t2c)
        truth = TexText(R"True answer: $D_S \approx 370 D_M$", t2c=t2c)

        guess.to_edge(UP)
        truth.next_to(guess, DOWN)

        truth.shift((guess["D_S"].get_x() - truth["D_S"].get_x()) * RIGHT)

        self.play(FadeIn(guess, 0.25 * UP))
        self.wait()
        self.play(FadeIn(truth, 0.25 * DOWN))
        self.wait()
