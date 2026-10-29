# ==============================================================================
# Scene:      Questions
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 181-292)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Questions.py Questions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Questions(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Lingering questions", font_size=72)
        title.add(Underline(title))
        title.to_edge(UP, buff=0.25)
        self.add(title)

        # Questions
        questions = self.get_questions()

        last_questions = questions[1:]
        last_questions.save_state()
        last_questions.set_height(6, about_edge=DL)

        for question in last_questions:
            self.play(FadeIn(question, 0.25 * UP))
            self.wait()
        self.wait()
        self.play(
            FadeIn(questions[0], shift=0.25 * DOWN),
            Restore(last_questions)
        )
        self.wait()

        # Check marks
        marks = VGroup(*(
            Checkmark(font_size=60).next_to(question[0], RIGHT).shift(0.15 * UP)
            for question in questions
        ))
        for mark in marks:
            mark.align_to(marks, RIGHT)

        # Crossing off
        cross_lines = VGroup()
        for question in questions:
            full_question = question[1]
            phrases = full_question.get_text().split("\n")
            cross_lines.add(VGroup(*(
                Line(LEFT, RIGHT).set_stroke(YELLOW, 3).replace(full_question[phrase], dim_to_match=0)
                for phrase in phrases
            )))

        # Mark off Q0
        self.play(
            Write(marks[0], stroke_color=GREEN),
            ShowCreation(cross_lines[0]),
        )
        self.wait()

        # Highlight question 3
        rect = SurroundingRectangle(questions[3])
        rect.set_stroke(YELLOW, 2)
        arrow = Vector(LEFT, stroke_color=YELLOW)
        arrow.next_to(rect, RIGHT)
        self.play(
            questions[:3].animate.set_opacity(0.5),
            ShowCreation(rect),
            FadeInFromPoint(arrow, ORIGIN),
        )
        self.wait()

        self.play(
            FadeOut(rect),
            FadeOut(arrow),
            ShowCreation(cross_lines[3]),
            Write(marks[3], stroke_color=GREEN),
            questions[:3].animate.set_opacity(1),
        )
        self.wait()

        # Question 1
        rect.set_stroke(opacity=0)
        arrow.set_stroke(opacity=0)
        self.play(
            rect.animate.surround(questions[1]).set_stroke(opacity=1),
            arrow.animate.next_to(questions[1], RIGHT).set_stroke(opacity=1),
        )
        self.wait()
        marks[1].set_fill(opacity=0)
        marks[1].set_stroke(GREEN, 2)
        self.play(
            FadeOut(rect),
            Write(marks[1]),
        )
        self.wait()

        # Question 2
        self.play(
            arrow.animate.next_to(questions[2], RIGHT)
        )
        self.wait()

    def get_questions(self):
        kw = dict(alignment="LEFT")
        question_texts = [
            "What exactly is wiggling?",
            "Why does sugar make light twist?",
            "Why does the twisting rate\ndepend on frequency?",
            "Why do we see colors\nin diagonal stripes?",
        ]
        questions = VGroup(*(
            VGroup(
                Text(f"Question #{n}:", **kw).set_fill(GREY_A),
                Text(text, **kw),
            ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            for n, text in enumerate(question_texts)
        ))
        questions.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        questions.set_height(6)
        questions.to_corner(DL)
        return questions
