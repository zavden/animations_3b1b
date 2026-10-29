# ==============================================================================
# Scene:      ThatsHorrifying
# Source:     videos/_2021/matrix_exp.py (lines 4026-4054)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThatsHorrifying.py ThatsHorrifying -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThatsHorrifying(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("You want us to\\\\do what?"),
            index=2,
            target_mode="pleading",
            added_anims=[LaggedStart(
                self.students[0].change("tired"),
                self.students[1].change("horrified"),
                self.teacher.change("guilty"),
                lag_ratio=0.5
            )]
        )
        for pi in self.pi_creatures:
            for eye in pi.eyes:
                # Why?
                eye.refresh_bounding_box()
        self.look_at(self.screen)
        self.wait(2)
        self.teacher_says(
            "Just wait",
            bubble_config={"height": 3, "width": 3.5},
            target_mode="tease"
        )
        self.play_student_changes(
            "pondering", "thinking", "hesitant",
            look_at=self.screen,
        )
        self.wait(3)
