# ==============================================================================
# Scene:      FalseVsTrueSurfaceAreaOverlay
# Source:     videos/_2022/visual_proofs/lies.py (lines 854-871)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FalseVsTrueSurfaceAreaOverlay.py FalseVsTrueSurfaceAreaOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FalseVsTrueSurfaceAreaOverlay(InteractiveScene):
    def construct(self):
        false_answer = VGroup(
            Text("False answer", color=RED),
            OldTex("\\pi^2 R^2"),
        )
        true_answer = VGroup(
            Text("True answer", color=GREEN),
            OldTex("4\\pi R^2"),
        )
        answers = VGroup(false_answer, true_answer)
        for answer in answers:
            answer.arrange(DOWN, buff=MED_LARGE_BUFF)
        answers.arrange(RIGHT, buff=LARGE_BUFF, aligned_edge=UP)

        self.play(FadeIn(false_answer))
        self.play(FadeIn(true_answer))
        self.wait()
