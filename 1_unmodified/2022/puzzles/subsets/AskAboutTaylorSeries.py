# ==============================================================================
# Scene:      AskAboutTaylorSeries
# Source:     videos/_2022/puzzles/subsets.py (lines 4951-4971)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutTaylorSeries.py AskAboutTaylorSeries -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutTaylorSeries(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("Can we use derivatives\\\\in some way?"),
            bubble_config=dict(width=4, height=3, direction=LEFT),
            index=2,
        )
        self.play(
            self.teacher.change("tease"),
            self.change_students(
                None, "confused", "thinking",
                look_at=self.students[2].bubble,
            ),
        )
        self.wait(4)
        self.teacher_says(
            "It's not a\nbad idea...",
            target_mode="hesitant",
        )
        self.play_student_changes("plain", "maybe", "pondering", look_at=self.screen)
        self.wait(4)
