# ==============================================================================
# Scene:      WaitScene
# Source:     videos/_2018/basel/basel.py (lines 3914-3927)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WaitScene.py WaitScene -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class WaitScene(TeacherStudentsScene):

    def construct(self):


        self.teacher_says(OldTex("{1\over 1^2}+{1\over 3^2}+{1\over 5^2}+{1\over 7^2}+\dots = {\pi^2 \over 8}!"))

        student_q = OldTexText("What about")
        full_sum = OldTex("{1\over 1^2}+{1\over 2^2}+{1\over 3^2}+{1\over 4^2}+\dots?")
        full_sum.next_to(student_q,RIGHT)
        student_q.add(full_sum)


        self.student_says(student_q, target_mode = "angry")
