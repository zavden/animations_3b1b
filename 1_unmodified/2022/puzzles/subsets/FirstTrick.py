# ==============================================================================
# Scene:      FirstTrick
# Source:     videos/_2022/puzzles/subsets.py (lines 4735-4759)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FirstTrick.py FirstTrick -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FirstTrick(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Here's our\nfirst trick",
            target_mode="tease",
            run_time=1
        )
        self.play_student_changes(
            "pondering", "thinking", "sassy",
            look_at=self.screen
        )
        self.wait(4)

        # Here
        self.student_says(
            OldTexText("Huh? What is $x$?"),
            index=2,
            target_mode="confused",
            look_at=self.teacher.eyes,
        )
        self.play_student_changes(
            "erm", "pondering",
            look_at=self.screen,
        )
        self.wait(4)
