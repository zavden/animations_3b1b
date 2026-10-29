# ==============================================================================
# Scene:      WhatIsInsideAndOutside
# Source:     videos/_2026/hairy_ball/supplements.py (lines 513-529)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatIsInsideAndOutside.py WhatIsInsideAndOutside -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatIsInsideAndOutside(TeacherStudentsScene):
    def construct(self):
        # Test
        stds = self.students
        morty = self.teacher

        self.play(
            stds[2].says(
                "Hang on, what\ndo you mean\n“paint the outside”?",
                mode="maybe",
                bubble_direction=LEFT
            ),
            stds[1].change("erm", self.screen),
            stds[0].change("pondering", self.screen),
            morty.change("tease")
        )
        self.wait(5)
