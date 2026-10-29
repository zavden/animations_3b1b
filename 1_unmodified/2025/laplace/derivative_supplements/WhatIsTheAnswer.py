# ==============================================================================
# Scene:      WhatIsTheAnswer
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 365-393)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatIsTheAnswer.py WhatIsTheAnswer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatIsTheAnswer(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            stds[1].says("Okay, okay, okay", mode="sassy"),
            stds[0].change("erm", stds[1].eyes),
            stds[2].change("hesitant", stds[1].eyes),
            morty.change("tease"),
        )
        self.wait(2)
        self.play(
            FadeOut(stds[1].bubble),
            stds[1].says("But...what is\nthe actual answer?", mode="maybe"),
            morty.change("guilty"),
        )
        self.wait()
        self.play(self.change_students("sassy", "erm", "confused", look_at=self.screen))
        self.wait(3)

        self.wait(2)
        self.play(
            FadeOut(stds[1].bubble),
            morty.change("raise_right_hand"),
            self.change_students("pondering", "pondering", "pondering", look_at=4 * UR)
        )
        self.wait(4)
