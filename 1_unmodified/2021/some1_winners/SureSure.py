# ==============================================================================
# Scene:      SureSure
# Source:     videos/_2021/some1_winners.py (lines 710-725)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SureSure.py SureSure -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SureSure(TeacherStudentsScene):
    def construct(self):
        self.students.flip().flip()
        self.teacher_says(
            "The point is \n not the winners",
            look_at=self.students[2].eyes,
            bubble_config={"height": 3, "width": 4}
        )
        self.play(PiCreatureSays(
            self.students[0],
            "Yeah, yeah, sure\n it isn't...",
            bubble_config={"height": 2, "width": 3}
        ))
        self.play_student_changes("sassy", "angry", "hesitant")
        self.play(self.teacher.change("guilty"))
        self.wait(4)
