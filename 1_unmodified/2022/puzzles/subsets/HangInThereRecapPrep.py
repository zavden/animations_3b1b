# ==============================================================================
# Scene:      HangInThereRecapPrep
# Source:     videos/_2022/puzzles/subsets.py (lines 5130-5148)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HangInThereRecapPrep.py HangInThereRecapPrep -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HangInThereRecapPrep(TeacherStudentsScene):
    def construct(self):
        # Hang on
        self.play_student_changes(
            "dejected", "tired", "concerned_musician",
            look_at=self.screen,
        )
        self.wait(2)
        self.teacher_says(
            "Hang in\nthere!",
            target_mode="tease",
            added_anims=[self.change_students("plain", "tease", "hesitant")]
        )
        self.wait(4)
        self.student_says(
            "Can you recap\nwhere we are?",
        )
        self.play_student_changes("confused", "thinking", added_anims=[self.teacher.change("happy")])
        self.wait(3)
