# ==============================================================================
# Scene:      RiemannHypothesisMention
# Source:     videos/_2022/puzzles/subsets.py (lines 400-412)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RiemannHypothesisMention.py RiemannHypothesisMention -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RiemannHypothesisMention(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "This is what the $1M\nRiemann Hypothesis\nis all about",
            bubble_config=dict(width=4, height=3),
            added_anims=[self.change_students(
                "erm", "happy", "thinking",
                look_at=self.screen,
            )]
        )
        self.wait(3)
        self.play_student_changes("pondering", "pondering", "tease")
        self.wait(3)
