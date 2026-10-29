# ==============================================================================
# Scene:      ComplainAboutSpecificity
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 531-549)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplainAboutSpecificity.py ComplainAboutSpecificity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplainAboutSpecificity(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            stds[1].says("But, that’s just\none example!", mode="angry"),
            stds[0].change("pondering", self.screen),
            stds[2].change("erm", self.screen),
            morty.change("guilty")
        )
        self.wait(3)
        self.play(
            stds[1].debubble("pondering"),
            morty.says("One with the\nseeds of generality"),
            stds[2].change("thinking")
        )
        self.wait(3)
