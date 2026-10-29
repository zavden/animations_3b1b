# ==============================================================================
# Scene:      HeresTheThing
# Source:     videos/_2021/quick_eigen.py (lines 2023-2057)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HeresTheThing.py HeresTheThing -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HeresTheThing(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Wait, why?",
            target_mode="raise_right_hand",
            look_at=self.screen,
            index=2,
        )
        self.play(
            self.change_students("maybe", "confused", "raise_right_hand", look_at=self.screen),
            self.teacher.change("happy"),
        )
        self.wait(3)
        self.teacher_says(
            OldTexText("Here's the thing..."),
            added_anims=[self.change_students("sassy", "plain", "hesitant")],
            target_mode="hesitant",
        )
        self.wait(2)
        self.play(RemovePiCreatureBubble(self.teacher, target_mode="raise_right_hand"))
        for pi in self.pi_creatures:
            for eye in pi.eyes:
                eye.refresh_bounding_box()
        self.look_at(self.screen)
        self.play_student_changes("tease", "thinking", "happy", look_at=self.screen)
        self.wait(3)
        words = OldTexText("Somewhat\\\\self-defeating")
        words.next_to(self.screen, RIGHT)
        words.shift(RIGHT)
        self.play(
            self.teacher.change("guilty"),
            self.change_students("sassy", "hesitant", "sassy"),
            Write(words),
        )
        self.wait(4)
