# ==============================================================================
# Scene:      ReferenceWorkedExample
# Source:     videos/_2025/laplace/main_supplements.py (lines 157-177)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceWorkedExample.py ReferenceWorkedExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceWorkedExample(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        rect = Rectangle(8, 1.5)
        rect.next_to(morty, UP).to_edge(RIGHT).shift(UP)
        rect.set_stroke(YELLOW, 2)
        self.play(
            morty.change("raise_left_hand", rect),
            self.change_students("pondering", "thinking", "erm", look_at=rect),
        )
        self.play(ShowCreation(rect))
        self.wait()
        self.play(
            morty.change("raise_right_hand", self.screen),
            FadeOut(rect),
            self.change_students("pondering", "pondering", "pondering", look_at=self.screen)
        )
        self.wait(7)
