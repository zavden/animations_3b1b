# ==============================================================================
# Scene:      AskHexagonQuestion
# Source:     videos/_2024/puzzles/supplements.py (lines 75-114)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskHexagonQuestion.py AskHexagonQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskHexagonQuestion(InteractiveScene):
    def construct(self):
        # Test
        question = Text("Can any tiling\n turn into any other?", font_size=60)
        question.to_corner(UL)

        arrow = Vector(2 * DOWN)
        arrow.next_to(question, DOWN)
        ifs = VGroup(Text("If no"), Text("If yes"))
        ifs.scale(0.75)
        ifs.next_to(arrow, RIGHT, SMALL_BUFF)
        ifs.set_submobject_colors_by_gradient(RED, GREEN)

        subquestions = VGroup(
            Text("How many connected\nsets are there?"),
            TexText(R"""
                Which two states are\\``farthest'' apart?
                \\ \quad \\
                How many moves\\away are they?
            """),
        )
        subquestions.next_to(arrow, DOWN)
        subquestions.set_color(GREY_A)

        self.play(Write(question))
        self.wait()
        self.play(
            GrowArrow(arrow),
            FadeIn(ifs[0], DOWN),
        )
        self.play(FadeIn(subquestions[0], lag_ratio=0.1))
        self.wait()
        self.play(
            FadeOut(VGroup(arrow.copy(), ifs[0], subquestions[0]), 3 * LEFT),
            GrowArrow(arrow),
            FadeIn(ifs[1], DOWN)
        )
        self.wait()
        self.play(FadeIn(subquestions[1], lag_ratio=0.1))
        self.wait()
