# ==============================================================================
# Scene:      ManyIterations
# Source:     videos/_2018/WindingNumber_G.py (lines 3014-3035)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl ManyIterations.py ManyIterations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/WindingNumber.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7



# ----- From _2018/WindingNumber_G.py -----

class ManyIterations(Scene):
    def construct(self):
        words = VGroup(*[
            OldTexText(word, alignment = "")
            for word in [
                "Winding numbers, v1",
                "Winding numbers, v2 \\\\ (center on domain coloring)",
                "Winding numbers, v3 \\\\ (clarify visuals of 2d functions)",
                "Winding numbers, v4 \\\\ (postpone topology examples for part 2)",
                "Winding numbers, v5 \\\\ (start down wrong path)",
            ]
        ])
        words.arrange(DOWN, buff = MED_LARGE_BUFF, aligned_edge = LEFT)
        words.scale(0.75)
        words.to_edge(RIGHT)

        self.add(words[0])
        for last_word, word in zip(words, words[1:]):
            cross = Cross(last_word)
            self.play(ShowCreation(cross))
            self.play(FadeIn(word))
        self.wait()
