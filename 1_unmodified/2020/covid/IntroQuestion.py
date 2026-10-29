# ==============================================================================
# Scene:      IntroQuestion
# Source:     videos/_2020/covid.py (lines 384-400)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroQuestion.py IntroQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroQuestion(Scene):
    def construct(self):
        questions = VGroup(
            OldTexText("What is exponential growth?"),
            OldTexText("Where does it come from?"),
            OldTexText("What does it imply?"),
            OldTexText("When does it stop?"),
        )
        questions.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)

        for question in questions:
            self.play(FadeIn(question, RIGHT))
            self.wait()
        self.play(LaggedStartMap(
            FadeOutAndShift, questions,
            lambda m: (m, DOWN),
        ))
