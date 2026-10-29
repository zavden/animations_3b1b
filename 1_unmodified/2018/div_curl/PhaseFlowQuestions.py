# ==============================================================================
# Scene:      PhaseFlowQuestions
# Source:     videos/_2018/div_curl.py (lines 3197-3210)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PhaseFlowQuestions.py PhaseFlowQuestions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PhaseFlowQuestions(Scene):
    def construct(self):
        questions = VGroup(
            OldTexText(
                "Which points does the flow \\\\" +
                "converge to?  Diverge away from?",
            ),
            OldTexText("Where are there cycles?"),
        )
        questions.arrange(DOWN, buff=LARGE_BUFF)
        questions.to_corner(UR)
        for question in questions:
            self.play(FadeInFromDown(question))
            self.wait(2)
