# ==============================================================================
# Scene:      IGotThis
# Source:     videos/_2020/chess.py (lines 1460-1473)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IGotThis.py IGotThis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IGotThis(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Pssh, I got this",
            target_mode="tease",
            look_at=self.screen,
            added_anims=[self.teacher.change, "happy", self.screen],
            run_time=2,
        )
        self.play_student_changes(
            "thinking", "pondering",
            look_at=self.screen
        )
        self.wait(6)
