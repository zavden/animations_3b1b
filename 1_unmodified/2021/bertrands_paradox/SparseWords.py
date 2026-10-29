# ==============================================================================
# Scene:      SparseWords
# Source:     videos/_2021/bertrands_paradox.py (lines 257-272)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SparseWords.py SparseWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SparseWords(Scene):
    def construct(self):
        words = Text("Sparser in the middle")
        words.to_edge(DOWN, buff=MED_LARGE_BUFF)
        arrow = Arrow(
            words.get_top(),
            [3.5, -0.5, 0],
        )
        arrow.set_color(YELLOW)
        words.set_color(YELLOW)

        self.play(
            Write(words, run_time=1),
            ShowCreation(arrow),
        )
        self.wait()
