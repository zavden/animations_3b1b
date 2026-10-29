# ==============================================================================
# Scene:      AssumingItsGood
# Source:     videos/_2021/newton_fractal.py (lines 1958-1970)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AssumingItsGood.py AssumingItsGood -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AssumingItsGood(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            OldTexText("Assuming this\\\\approximation\\\\is decent...", font_size=42),
            bubble_config={
                "height": 3, "width": 4,
            }
        )
        self.play_student_changes(
            "pondering", "pondering", "tease",
            look_at=self.screen
        )
        self.wait(3)
