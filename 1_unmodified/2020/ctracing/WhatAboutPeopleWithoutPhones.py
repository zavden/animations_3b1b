# ==============================================================================
# Scene:      WhatAboutPeopleWithoutPhones
# Source:     videos/_2020/ctracing.py (lines 309-333)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatAboutPeopleWithoutPhones.py WhatAboutPeopleWithoutPhones -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatAboutPeopleWithoutPhones(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What about people\\\\without phones?",
            target_mode="sassy",
            added_anims=[self.teacher.change, "guilty"]
        )
        self.play_student_changes("angry", "angry", "sassy")
        self.wait()
        self.play(self.teacher.change, "tease")
        self.wait()

        words = VectorizedPoint()
        words.scale(1.5)
        words.to_corner(UL)

        self.play(
            FadeInFromDown(words),
            RemovePiCreatureBubble(self.students[2]),
            *[
                ApplyMethod(pi.change, "pondering", words)
                for pi in self.pi_creatures
            ]
        )
        self.wait(5)
