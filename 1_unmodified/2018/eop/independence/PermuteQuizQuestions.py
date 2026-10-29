# ==============================================================================
# Scene:      PermuteQuizQuestions
# Source:     videos/_2018/eop/independence.py (lines 3106-3130)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PermuteQuizQuestions.py PermuteQuizQuestions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_quiz(*questions):
    q_mobs = VGroup(*list(map(TexText, [
        "%d. %s"%(i+1, question)
        for i, question in enumerate(questions)
    ])))
    q_mobs.arrange(
        DOWN, 
        buff = MED_LARGE_BUFF,
        aligned_edge = LEFT, 
    )
    content = VGroup(
        OldTexText("Quiz").scale(1.5),
        Line(q_mobs.get_left(), q_mobs.get_right()),
        q_mobs
    )
    content.arrange(DOWN, buff = MED_SMALL_BUFF)
    rect = SurroundingRectangle(content, buff = MED_LARGE_BUFF)
    rect.shift(MED_SMALL_BUFF*DOWN)
    rect.set_color(WHITE)
    quiz = VGroup(rect, content)
    quiz.questions = q_mobs
    quiz.scale(0.7)
    return quiz


class PermuteQuizQuestions(Scene):
    def construct(self):
        quiz = get_quiz(
            "Define ``Brachistochrone''",
            "Define ``Tautochrone''",
            "Define ``Cycloid''",
        )
        questions = [
            VGroup(*q[2:])
            for q in quiz.questions
        ]
        colors = [BLUE, GREEN, RED]
        for color, question in zip(colors, questions):
            question.set_color(color)
        quiz.scale(2)

        self.add(quiz)
        self.wait()
        for m1, m2 in it.combinations(questions, 2):
            self.play(
                m1.move_to, m2, LEFT,
                m2.move_to, m1, LEFT,
                path_arc = np.pi
            )
            self.wait()
