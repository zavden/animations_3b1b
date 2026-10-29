# ==============================================================================
# Scene:      QuestionsFromPatrons
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1209-1266)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuestionsFromPatrons.py QuestionsFromPatrons -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuestionsFromPatrons(InteractiveScene):
    def construct(self):
        # Questions
        title = Text("Viewer questions about the index of refraction", font_size=60)
        title.to_edge(UP)
        title.add(Underline(title))
        title.set_color(BLUE)

        questions = BulletedList(
            "Why does slowing imply bending?",
            "What causes birefringence?",
            "What's the end of the barber pole explanation?",
            "How can the index of refraction be lower than 1?",
            buff=0.75
        )
        questions.next_to(title, DOWN, buff=1.0)

        self.play(
            FadeIn(title, lag_ratio=0.1),
            LaggedStartMap(FadeIn, questions, shift=0.5 * DOWN, lag_ratio=0.25)
        )
        self.wait()

        # Higlight last three
        last_three = questions[1:]
        highlight_rect = SurroundingRectangle(last_three, buff=0.25)
        highlight_rect.set_stroke(YELLOW, 2)
        grey_rect = highlight_rect.copy().set_stroke(width=0).set_fill(GREY_E, 1)
        back_rect = FullScreenRectangle().set_fill(BLACK, 0.9)
        self.add(back_rect, grey_rect, highlight_rect, last_three)
        self.play(
            FadeIn(back_rect),
            FadeIn(grey_rect),
            DrawBorderThenFill(highlight_rect)
        )
        self.wait()
        self.play(FadeOut(back_rect), FadeOut(grey_rect), FadeOut(highlight_rect))

        # Each question
        background = FullScreenRectangle()
        background.set_fill(interpolate_color(GREY_E, BLACK, 0.5), 1)

        for question in questions:
            question.save_state()
            question.target = question.generate_target()
            question.target[0].scale(0, about_point=question[1].get_left()).set_opacity(0)
            question.target.center().to_edge(UP)

            self.add(background, question)
            self.play(
                FadeIn(background),
                MoveToTarget(question),
            )
            self.wait()
            self.play(
                Restore(question),
                FadeOut(background),
            )
