# ==============================================================================
# Scene:      AristarchusSunSizeEstimate
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 978-993)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AristarchusSunSizeEstimate.py AristarchusSunSizeEstimate -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AristarchusSunSizeEstimate(InteractiveScene):
    def construct(self):
        # Mostly copied from above
        t2c = {"R_S": YELLOW, "R_E": BLUE}
        guess = TexText("Aristarchus's Guess: $R_S = 7 R_E$", t2c=t2c)
        truth = TexText(R"True answer: $R_S \approx 109 R_E$", t2c=t2c)

        guess.to_edge(UP)
        truth.next_to(guess, DOWN)

        truth.shift((guess["R_S"].get_x() - truth["R_S"].get_x()) * RIGHT)

        self.play(FadeIn(guess, 0.25 * UP))
        self.wait()
        self.play(FadeIn(truth, 0.25 * DOWN))
        self.wait()
