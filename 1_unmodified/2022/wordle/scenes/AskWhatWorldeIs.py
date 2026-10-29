# ==============================================================================
# Scene:      AskWhatWorldeIs
# Source:     videos/_2022/wordle/scenes.py (lines 1064-1078)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhatWorldeIs.py AskWhatWorldeIs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskWhatWorldeIs(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What is Wordle?",
            index=0,
            target_mode="raise_left_hand",
            added_anims=[
                self.teacher.change("tease")
            ]
        )
        self.play_student_changes(
            "raise_left_hand", "hesitant", "happy",
            look_at=self.students[0].bubble,
        )
        self.wait(3)
