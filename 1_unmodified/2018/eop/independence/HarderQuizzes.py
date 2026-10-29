# ==============================================================================
# Scene:      HarderQuizzes
# Source:     videos/_2018/eop/independence.py (lines 1236-1262)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HarderQuizzes.py HarderQuizzes -w -m --fps 15
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


class HarderQuizzes(Scene):
    def construct(self):
        quizzes = VGroup(
            get_quiz(
                "Find all primes $p$ \\\\ where $p+2$ is prime.",
                "Find all primes $p$ \\\\ where $2^{p}-1$ is prime.",
                "Solve $\\zeta(s) = 0$",
            ),
            get_quiz(
                "Find $S$ such that \\\\ $\\#\\mathds{N} < \\#S < \\#\\mathcal{P}(\\mathds{N})$",
                "Describe ``forcing''",
                "Prove from ZFC that $S \\notin S$.",
            ),
        )
        quizzes.arrange(RIGHT)
        quizzes.to_edge(DOWN)
        crosses = VGroup(*[
            Cross(quiz.questions[0])
            for quiz in quizzes
        ])

        for quiz in quizzes:
            self.play(FadeIn(quiz))
        self.wait()
        for cross in crosses:
            self.play(ShowCreation(cross))
        self.wait()
