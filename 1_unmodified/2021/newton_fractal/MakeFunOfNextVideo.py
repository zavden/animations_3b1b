# ==============================================================================
# Scene:      MakeFunOfNextVideo
# Source:     videos/_2021/newton_fractal.py (lines 4542-4566)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MakeFunOfNextVideo.py MakeFunOfNextVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MakeFunOfNextVideo(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("``Next part''...I've\\\\heard that before."),
            target_mode="sassy",
            index=2,
            added_anims=[LaggedStart(
                self.teacher.change("guilty"),
                self.students[0].change("sassy"),
                self.students[1].change("hesitant"),
            )]
        )
        self.wait()
        self.teacher_says(
            OldTexText("Wait, for real\\\\this time!"),
            bubble_config={
                "height": 3,
                "width": 3,
            },
            target_mode="speaking",
            added_anims=[
                self.students[0].change("hesitant"),
            ]
        )
        self.wait(3)
