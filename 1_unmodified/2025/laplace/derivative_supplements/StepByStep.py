# ==============================================================================
# Scene:      StepByStep
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 310-330)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StepByStep.py StepByStep -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StepByStep(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(1000)

        self.background.fade(0.5)

        self.play(
            morty.change("raise_right_hand"),
            self.change_students("confused", "maybe", "erm", look_at=self.screen)
        )
        self.wait()
        self.play(
            morty.change("tease"),
            self.change_students("pondering", "thinking", "pondering", look_at=morty.eyes)
        )
        self.wait()
        self.look_at(self.screen)
        self.wait(4)
