# ==============================================================================
# Scene:      PossibleYetProbabilityZero
# Source:     videos/_2020/beta/beta2.py (lines 1973-1988)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PossibleYetProbabilityZero.py PossibleYetProbabilityZero -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PossibleYetProbabilityZero(Scene):
    def construct(self):
        poss = OldTexText("Possible")
        prob = OldTexText("Probability = 0")
        total = OldTexText("P(dart hits somewhere) = 1")
        # total[1].next_to(total[0][0], RIGHT)
        words = VGroup(poss, prob, total)
        words.scale(1.5)
        words.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)

        self.play(Write(poss, run_time=0.5))
        self.wait()
        self.play(FadeIn(prob, UP))
        self.wait()
        self.play(FadeIn(total, UP))
        self.wait()
