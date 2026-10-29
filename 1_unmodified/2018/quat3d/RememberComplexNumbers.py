# ==============================================================================
# Scene:      RememberComplexNumbers
# Source:     videos/_2018/quat3d.py (lines 860-887)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RememberComplexNumbers.py RememberComplexNumbers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RememberComplexNumbers(TeacherStudentsScene):
    def construct(self):
        complex_number = OldTex(
            "\\cos(\\theta) + \\sin(\\theta)i",
            tex_to_color_map={
                "\\cos(\\theta)": GREEN,
                "\\sin(\\theta)": RED
            }
        )
        complex_number.scale(1.2)
        complex_number.next_to(self.students, UP, MED_LARGE_BUFF)

        self.teacher_says(
            "Remember how \\\\ complex numbers \\\\ compute rotations"
        )
        self.play_all_student_changes("pondering")
        self.wait()
        self.play(
            FadeInFromDown(complex_number),
            self.change_students(
                "thinking", "confused", "happy",
                look_at=complex_number.get_center() + UP
            ),
            run_time=2
        )
        self.play_student_changes(
        )
        self.wait(5)
