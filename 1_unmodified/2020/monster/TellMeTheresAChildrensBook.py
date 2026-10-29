# ==============================================================================
# Scene:      TellMeTheresAChildrensBook
# Source:     videos/_2020/monster.py (lines 4110-4119)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TellMeTheresAChildrensBook.py TellMeTheresAChildrensBook -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TellMeTheresAChildrensBook(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Please tell me\\\\there's a children's\\\\book about this!",
            target_mode="surprised",
            added_anims=[self.teacher.change, "tease"]
        )
        self.play_student_changes("happy", "coin_flip_1", look_at=self.screen)
        self.look_at(self.screen)
        self.wait(5)
