# ==============================================================================
# Scene:      IsItUseful
# Source:     videos/_2020/monster.py (lines 1337-1349)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IsItUseful.py IsItUseful -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IsItUseful(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Is any of\\\\this useful?",
            index=2,
            target_mode="sassy",
            added_anims=[self.teacher.change, "guilty"]
        )
        self.play_student_changes("angry", "confused")
        self.wait(3)
        self.teacher_says("Extremely!")
        self.play_student_changes("pondering", "thinking", "pondering", look_at=self.screen)
        self.wait(4)
