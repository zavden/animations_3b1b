# ==============================================================================
# Scene:      TwoLevels
# Source:     videos/_2025/laplace/main_supplements.py (lines 13-25)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoLevels.py TwoLevels -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoLevels(InteractiveScene):
    def construct(self):
        # Test
        words = VGroup(
            Text("Solve equations"),
            Text("See what it’s doing"),
        )
        words.scale(1.5)
        for word, y in zip(words, (2, -2)):
            word.set_y(y)
            word.to_edge(LEFT, buff=LARGE_BUFF)
            self.play(Write(word))
            self.wait()
