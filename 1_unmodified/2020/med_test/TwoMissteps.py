# ==============================================================================
# Scene:      TwoMissteps
# Source:     videos/_2020/med_test.py (lines 7019-7040)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoMissteps.py TwoMissteps -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoMissteps(Scene):
    def construct(self):
        words = VGroup(
            OldTexText(
                "Misstep 1: ",
                "Fail to consider the prevalence."
            ),
            OldTexText(
                "Misstep 2: ",
                "Assume prior = prevalence"
            ),
        )
        words[0][0].set_color(YELLOW)
        words[1][0].set_color(BLUE)
        words.scale(1.5)
        words.arrange(DOWN, buff=1, aligned_edge=LEFT)
        words.to_edge(LEFT)

        self.add(words)

        # Embed
        self.embed()
