# ==============================================================================
# Scene:      LetsLookAtOneAnswer
# Source:     videos/_2020/beta/beta1.py (lines 599-610)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LetsLookAtOneAnswer.py LetsLookAtOneAnswer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LetsLookAtOneAnswer(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        self.teacher_says(
            "Let me show you\\\\one answer.",
            added_anims=[
                self.change_students("pondering", "thinking", "pondering")
            ]
        )
        self.look_at(self.screen)
        self.play_all_student_changes("thinking", look_at=self.screen)
        self.wait(4)
