# ==============================================================================
# Scene:      QuestionsOnTheStateVector
# Source:     videos/_2025/grover/qc_supplements.py (lines 419-456)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuestionsOnTheStateVector.py QuestionsOnTheStateVector -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuestionsOnTheStateVector(TeacherStudentsScene):
    def construct(self):
        # React
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)  # Make it 10k?
        morty = self.teacher
        stds = self.students
        self.play(
            morty.change("hesitant"),
            self.change_students("pleading", "confused", "erm", look_at=self.screen)
        )
        self.wait(3)

        # Questions
        self.play(
            stds[0].says("But...\nwhat is it?", mode="maybe", look_at=morty.eyes)
        )
        self.wait()
        self.add(Point())
        self.play(
            stds[1].says("Why square things?", mode="raise_right_hand", look_at=morty.eyes)
        )
        self.wait(3)

        # Reference Complex
        expr = Tex(R"\mathds{R}^n \text{ vs. } \mathds{C}^n")
        expr.move_to(self.hold_up_spot, DOWN)

        self.play(
            morty.change("raise_right_hand"),
            FadeIn(expr, UP),
            stds[0].debubble(mode="sassy"),
            stds[1].debubble(mode="erm"),
            stds[2].change("confused", look_at=expr)
        )
        self.wait(3)
        self.play(self.change_students("pondering", "pondering", "pondering", look_at=self.screen))
        self.wait(3)
