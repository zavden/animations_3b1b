# ==============================================================================
# Scene:      AskAboutFractals
# Source:     videos/_2021/newton_fractal.py (lines 1402-1429)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutFractals.py AskAboutFractals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutFractals(TeacherStudentsScene):
    def construct(self):
        self.screen.set_height(4, about_edge=UL)
        self.screen.set_fill(BLACK, 1)
        self.add(self.screen)
        self.student_says(
            "Fractals?",
            target_mode="raise_right_hand",
            index=2,
            added_anims=[
                self.students[0].change("confused"),
                self.students[1].change("sassy"),
            ]
        )
        self.wait()
        self.teacher_says(
            OldTexText("We're getting\\\\there"),
            bubble_config={
                "height": 3,
                "width": 4,
            },
            target_mode="happy"
        )
        self.play_all_student_changes(
            "pondering",
            look_at=self.screen
        )
        self.wait(2)
