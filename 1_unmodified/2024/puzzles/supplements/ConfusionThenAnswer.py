# ==============================================================================
# Scene:      ConfusionThenAnswer
# Source:     videos/_2024/puzzles/supplements.py (lines 632-655)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConfusionThenAnswer.py ConfusionThenAnswer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConfusionThenAnswer(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.play(
            morty.change("guilty"),
            self.change_students("maybe", "tired", "concentrating", look_at=self.screen)
        )
        self.wait()

        # Answer
        answer = TexText(R"Maximum number \\ of moves: $N^4$")
        answer.next_to(stds[2].get_corner(UR), UP, buff=LARGE_BUFF)
        answer["N^4"].set_color(YELLOW)

        self.play(
            stds[2].change("raise_right_hand", answer)
        )
        self.play(
            self.change_students("pondering", "pondering", "raise_right_hand", look_at=answer),
            morty.change("tease"),
            FadeIn(answer, 0.5 * UP)
        )
        self.wait(5)
