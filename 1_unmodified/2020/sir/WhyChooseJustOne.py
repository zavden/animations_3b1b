# ==============================================================================
# Scene:      WhyChooseJustOne
# Source:     videos/_2020/sir.py (lines 2905-2926)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyChooseJustOne.py WhyChooseJustOne -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyChooseJustOne(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Why choose\\\\just one?",
            target_mode="sassy",
            added_anims=[self.teacher.change, "thinking"],
            run_time=1,
        )
        self.play(
            self.change_students(
                "confused", "confused", "sassy",
            ),
        )
        self.wait(2)
        self.teacher_says(
            "For science!", target_mode="hooray",
            look_at=self.students[2].eyes,
        )
        self.play_student_changes("hesitant", "hesitant", "hesitant")
        self.wait(3)

        self.embed()
