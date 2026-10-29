# ==============================================================================
# Scene:      QuestionMorph
# Source:     videos/_2022/puzzles/subsets.py (lines 4711-4723)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuestionMorph.py QuestionMorph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuestionMorph(InteractiveScene):
    def construct(self):
        question = OldTexText(
            "How many subsets are there\\\\",
            "with a sum divisible by 5", "?"
        )
        self.play(Write(question))
        self.wait(2)
        self.play(
            question[1].animate.scale(0.75).set_opacity(0.5).to_corner(DL),
            question[2].animate.next_to(question[0], RIGHT, SMALL_BUFF),
        )
        self.wait()
