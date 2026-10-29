# ==============================================================================
# Scene:      ReferenceAnalyticContinuation
# Source:     videos/_2025/laplace/main_supplements.py (lines 596-615)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceAnalyticContinuation.py ReferenceAnalyticContinuation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceAnalyticContinuation(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(1000)
        words = Text("Analytic\nContinuation", font_size=60)
        words.next_to(morty, UP, LARGE_BUFF)
        words.match_x(morty.get_left())

        self.play(
            self.change_students("pondering", "pondering", 'pondering', look_at=self.screen),
            morty.change("raise_right_hand"),
            Write(words),
        )
        self.wait(4)
        self.play(self.change_students("erm", "thinking", "pondering", look_at=self.screen))
        self.wait(4)
        self.play(self.change_students("pondering", "tease", "thinking", look_at=self.screen))
        self.wait(4)
