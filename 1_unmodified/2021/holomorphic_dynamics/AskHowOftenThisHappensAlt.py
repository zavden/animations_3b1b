# ==============================================================================
# Scene:      AskHowOftenThisHappensAlt
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2287-2327)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskHowOftenThisHappensAlt.py AskHowOftenThisHappensAlt -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskHowOftenThisHappensAlt(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("How often does\\\\this happen?"),
            bubble_config={
                "height": 3,
                "width": 4,
            },
            index=0,
        )
        self.play(
            self.teacher.change("raise_right_hand", 3 * UR),
            self.change_students(
                "raise_left_hand", "pondering", "pondering",
                look_at=3 * UR,
            )
        )
        self.play_student_changes(
            "raise_left_hand", "erm", "erm",
            look_at=3 * UR,
        )
        self.wait()
        self.play(self.teacher.change("tease", 3 * UR))
        self.play_student_changes(
            "confused", "pondering", "thinking",
            look_at=3 * UR,
        )
        self.wait(8)
        return

        self.wait(2)
        self.play(
            PiCreatureSays(
                self.teacher, "You'll like this",
                target_mode="tease",
                run_time=1,
            ),
            self.students[1].change("thinking", self.teacher.eyes),
            self.students[2].change("thinking", self.teacher.eyes),
        )
        self.wait(2)
