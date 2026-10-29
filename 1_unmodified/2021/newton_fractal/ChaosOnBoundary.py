# ==============================================================================
# Scene:      ChaosOnBoundary
# Source:     videos/_2021/newton_fractal.py (lines 3094-3104)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ChaosOnBoundary.py ChaosOnBoundary -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ChaosOnBoundary(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            OldTexText("Chaos at\\\\the boundary"),
            bubble_config={
                "height": 3,
                "width": 3,
            }
        )
        self.play_all_student_changes("pondering", look_at=self.screen)
        self.wait(3)
