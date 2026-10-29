# ==============================================================================
# Scene:      HowDoYouKnowWhichAxis
# Source:     videos/_2025/grover/clarification.py (lines 146-161)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowDoYouKnowWhichAxis.py HowDoYouKnowWhichAxis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowDoYouKnowWhichAxis(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        self.play(
            morty.change("guilty"),
            stds[2].says("Doesn't this assumes\nknowing the key value?", mode="angry", bubble_direction=LEFT),
            stds[0].change("confused", look_at=self.screen),
            stds[1].change("pleading", look_at=self.screen),
        )
        self.wait()
        self.look_at(self.screen)
        self.wait(5)
        self.play(self.change_students("erm", "confused", "sassy"))
        self.wait(5)
