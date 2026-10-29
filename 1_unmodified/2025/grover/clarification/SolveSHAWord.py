# ==============================================================================
# Scene:      SolveSHAWord
# Source:     videos/_2025/grover/clarification.py (lines 719-730)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SolveSHAWord.py SolveSHAWord -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SolveSHAWord(InteractiveScene):
    def construct(self):
        words = VGroup(
            TexText(R"Solve for ${x}$"),
            Tex(R"\text{SHA256}({x}) = 0"),
        )
        words.set_color(GREY_B)
        for word in words:
            word["{x}"].set_color(YELLOW)
        words.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        self.play(Write(words))
        self.wait()
