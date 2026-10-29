# ==============================================================================
# Scene:      QuadraticFormula
# Source:     videos/_2020/ldm.py (lines 72-96)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuadraticFormula.py QuadraticFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuadraticFormula(TeacherStudentsScene):
    def construct(self):
        formula = OldTex(
            "\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
        )
        formula.next_to(self.students, UP, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        self.add(formula)

        self.play_student_changes(
            "angry", "tired", "sad",
            look_at=formula,
        )
        self.teacher_says(
            "It doesn't have\\\\to be this way.",
            bubble_config={
                "width": 4,
                "height": 3,
            }
        )
        self.wait(5)
        self.play_student_changes(
            "pondering", "thinking", "erm",
            look_at=formula
        )
        self.wait(12)
