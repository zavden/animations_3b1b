# ==============================================================================
# Scene:      TryOtherExamples
# Source:     videos/_2017/eoc/chapter6.py (lines 1807-1830)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TryOtherExamples.py TryOtherExamples -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TryOtherExamples(TeacherStudentsScene):
    def construct(self):
        formula = OldTex("\\sin(x)y^2 = x")
        formula.next_to(
            self.get_teacher().get_corner(UP+LEFT), UP,
            buff = MED_LARGE_BUFF,
            aligned_edge = RIGHT
        )


        self.teacher_says(
            """Nothing special
            about $x^2 + y^2 = 25$"""
        )
        self.wait()
        self.play(RemovePiCreatureBubble(
            self.get_teacher(),
            target_mode = "raise_right_hand"
        ))
        self.play(Write(formula, run_time = 1))
        self.play_student_changes(*["pondering"]*3)
        self.wait(2)
        self.play(formula.to_corner, UP+LEFT)
        self.wait()
