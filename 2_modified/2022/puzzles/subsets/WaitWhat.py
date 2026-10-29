# ==============================================================================
# Scene:      WaitWhat
# Source:     videos/_2022/puzzles/subsets.py (lines 4801-4817)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WaitWhat.py WaitWhat -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - target_mode='confused' was inside OldTexText (which does not accept it); it is passed to student_says, which was the intent
# ==============================================================================

from manim_imports_ext import *

class WaitWhat(TeacherStudentsScene):
    def construct(self):
        # CHANGE: target_mode="confused" was inside OldTexText (Mobject no longer accepts unknown kwargs); the intent is to pass it to student_says
        self.student_says(
            OldTexText("Wait...can you\\\\explain that?"),
            target_mode="confused",
            added_anims=[
                self.teacher.change("guilty"),
                self.students[0].change("erm", self.screen),
                self.students[1].change("maybe", self.screen),
            ]
        )
        self.wait()
        self.look_at(self.screen)
        self.play_student_changes(
            "pondering", "confused", "maybe",
            look_at=self.screen,
        )
        self.wait(2)
