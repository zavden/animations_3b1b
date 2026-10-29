# ==============================================================================
# Scene:      WhatIsItTryingToDo2
# Source:     videos/_2025/laplace/main_supplements.py (lines 93-122)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatIsItTryingToDo2.py WhatIsItTryingToDo2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatIsItTryingToDo2(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(1000)

        self.play(
            morty.change("raise_right_hand", look_at=3 * UP),
            self.change_students("thinking", "confused", "pondering", look_at=3 * UR)
        )
        self.wait(2)
        self.play(LaggedStart(
            stds[0].change("pondering", morty.eyes),
            stds[1].says("What does it\nactually do?", mode="raise_left_hand", look_at=morty.eyes),
            stds[2].change("hesitant", morty.eyes),
            morty.change("tease"),
            lag_ratio=0.3
        ))
        self.wait(4)

        # Test2
        self.play(
            stds[0].change("pondering", 3 * UP),
            stds[1].debubble(look_at=3 * UP),
            stds[2].change("pondering", 3 * UP),
            morty.change("raise_right_hand"),
        )
        self.wait(3)
