# ==============================================================================
# Scene:      UnrelatedIdeas
# Source:     videos/_2021/newton_fractal.py (lines 3541-3570)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnrelatedIdeas.py UnrelatedIdeas -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UnrelatedIdeas(TeacherStudentsScene):
    def construct(self):
        self.screen.set_height(4, about_edge=UL)
        self.add(self.screen)

        self.play_student_changes(
            "tease", "thinking", "raise_right_hand",
            look_at=self.screen,
            added_anims=[self.teacher.change("happy")]
        )
        self.wait(2)
        self.teacher_says(
            OldTexText("Unrelated\\\\ideas"),
            bubble_config={
                "height": 3,
                "width": 4,
            },
            added_anims=[
                s.change("sassy", self.teacher.eyes)
                for s in self.students
            ]
        )
        self.play(LaggedStart(
            self.students[2].change("angry"),
            self.teacher.change("guilty"),
            lag_ratio=0.7,
        ))
        self.wait(2)

        self.embed()
