# ==============================================================================
# Scene:      AskAboutAveraging
# Source:     videos/_2021/shadows.py (lines 726-782)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutAveraging.py AskAboutAveraging -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutAveraging(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        sts = self.students
        tch = self.teacher

        self.play_student_changes(
            "maybe", "thinking", "erm",
            look_at=self.screen,
            added_anims=[self.teacher.change("raise_right_hand", self.screen)]
        )
        self.wait(3)
        self.play(
            PiCreatureBubbleIntroduction(
                sts[2], OldTexText("What does that\\\\mean, exactly?"),
                target_mode="hesitant",
                look_at=self.screen,
                bubble_config={"direction": LEFT}
            ),
            LaggedStart(
                sts[0].change("confused", self.screen),
                sts[1].change("pondering", self.screen),
                tch.change("tease", sts[2].eyes),
            )
        )
        self.wait(4)
        self.student_says(
            "Can we do an experiment?",
            target_mode="raise_left_hand",
            index=1,
        )
        self.wait(4)
        self.student_says(
            OldTexText("But what defines a\\\\``random'' toss?"),
            look_at=self.screen,
            target_mode="hesitant",
            index=2,
            added_anims=[
                self.teacher.change("guilty"),
                self.students[0].change("erm"),
            ]
        )
        self.wait(4)
        self.play(LaggedStart(
            self.students[0].change("pondering", self.screen),
            self.students[1].change("maybe", self.screen),
            self.teacher.change("tease", self.screen),
        ))
        self.wait(2)
        self.teacher_says(OldTexText("Hold off until\\\\the end"))
        self.wait(3)
        self.play_student_changes(
            "thinking", "tease", "pondering",
            look_at=self.screen,
            added_anims=[self.teacher.change("tease", self.students)]
        )
        self.wait(4)
