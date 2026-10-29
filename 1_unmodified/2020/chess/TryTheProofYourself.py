# ==============================================================================
# Scene:      TryTheProofYourself
# Source:     videos/_2020/chess.py (lines 3493-3512)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TryTheProofYourself.py TryTheProofYourself -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TryTheProofYourself(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Can you predict\\\\the proof?",
            target_mode="hooray",
            bubble_config={
                "height": 3,
                "width": 3,
            },
        )
        self.teacher.bubble.set_fill(opacity=0)
        self.play_student_changes(
            "pondering", "thinking", "confused",
            look_at=self.screen,
        )
        self.wait(3)
        self.play_student_changes("thinking", "pondering", "erm", look_at=self.screen)
        self.wait(4)
        self.play_student_changes("tease", "pondering", "thinking", look_at=self.screen)
        self.wait(5)
