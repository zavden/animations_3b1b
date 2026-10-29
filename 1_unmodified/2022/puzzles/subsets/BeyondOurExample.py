# ==============================================================================
# Scene:      BeyondOurExample
# Source:     videos/_2022/puzzles/subsets.py (lines 4762-4777)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BeyondOurExample.py BeyondOurExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BeyondOurExample(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Generating functions\n"
            "are useful beyond\n"
            "our one example.",
            bubble_config=dict(width=4, height=3),
            added_anims=[self.change_students(
                "happy", "jamming", "tease",
                look_at=self.screen,
            )]
        )
        self.wait(3)
        self.play(self.teacher.change("tease"))
        self.play_student_changes("thinking", "tease", "tease")
        self.wait(2)
