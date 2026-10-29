# ==============================================================================
# Scene:      StepsOfTheAlgorithm
# Source:     videos/_2019/clacks/question.py (lines 1005-1050)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StepsOfTheAlgorithm.py StepsOfTheAlgorithm -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StepsOfTheAlgorithm(TeacherStudentsScene):
    def construct(self):
        steps = self.get_steps()
        steps.arrange(
            DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        steps.to_corner(UL)
        steps.scale(0.8)

        for step in steps:
            self.play(
                FadeInFromDown(step[0]),
                self.teacher.change, "raise_right_hand"
            )
            self.play(
                Write(step[1], run_time=2),
                self.change_students(
                    *["pondering"] * 3,
                    look_at=step,
                )
            )
            self.wait()
        self.play_student_changes(
            "sassy", "erm", "confused",
            look_at=steps,
            added_anims=[self.teacher.change, "happy"]
        )
        self.wait(3)

    def get_steps(self):
        return VGroup(
            OldTexText("Step 1:", "Implement a physics engine"),
            OldTexText(
                "Step 2:",
                "Choose the number of digits, $d$,\\\\"
                "of $\\pi$ that you want to compute"
            ),
            OldTexText(
                "Step 3:",
                "Set one mass to $100^{d - 1}$,\\\\"
                "the other to $1$"
            ),
            OldTexText("Step 4:", "Count collisions"),
        )
