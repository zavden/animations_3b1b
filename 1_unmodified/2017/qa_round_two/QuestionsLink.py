# ==============================================================================
# Scene:      QuestionsLink
# Source:     videos/_2017/qa_round_two.py (lines 159-165)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuestionsLink.py QuestionsLink -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuestionsLink(Scene):
    def construct(self):
        link = OldTexText("https://3b1b.co/questions")
        link.set_width(FRAME_WIDTH)
        link.to_edge(DOWN)
        self.play(Write(link))
        self.wait()
