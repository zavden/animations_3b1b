# ==============================================================================
# Scene:      HowDoYouCompute
# Source:     videos/_2022/borwein/supplements.py (lines 422-442)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HowDoYouCompute.py HowDoYouCompute -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - student_says(mode=...) -> target_mode (student_says does not accept mode)
# ==============================================================================

from manim_imports_ext import *

class HowDoYouCompute(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.student_says(
            "But how do you\ncompute this\nFourier Transform?",
            # CHANGE: student_says receives target_mode (not mode)
            target_mode="angry",
            run_time=2
        )
        self.play(
            morty.change("guilty"),
            stds[0].change("confused", self.screen),
            stds[1].change("maybe", self.screen),
        )
        self.wait(2)
        self.play(
            stds[2].debubble(),
            morty.says("We'll get there"),
        )
        self.play(self.change_students("erm", "hesitant", "hesitant"))
        self.wait(2)
