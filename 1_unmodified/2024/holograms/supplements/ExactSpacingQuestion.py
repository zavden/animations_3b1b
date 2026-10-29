# ==============================================================================
# Scene:      ExactSpacingQuestion
# Source:     videos/_2024/holograms/supplements.py (lines 879-894)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExactSpacingQuestion.py ExactSpacingQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExactSpacingQuestion(InteractiveScene):
    def construct(self):
        # Test
        question = Text("What is the exact spacing?", font_size=72)
        question.set_backstroke()
        question.to_edge(UP)
        subq = TexText(R"As a function of $\theta'$")
        subq.set_color(GREY_A)

        self.play(Write(question, stroke_color=WHITE))
        self.wait()
        self.play(question.animate.scale(48 / 72).set_x(-0.25 * FRAME_WIDTH))
        self.wait()
        subq.next_to(question, DOWN)
        self.play(FadeIn(subq, 0.5 * DOWN))
        self.wait()
