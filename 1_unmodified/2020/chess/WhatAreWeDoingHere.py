# ==============================================================================
# Scene:      WhatAreWeDoingHere
# Source:     videos/_2020/chess.py (lines 1039-1048)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatAreWeDoingHere.py WhatAreWeDoingHere -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatAreWeDoingHere(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Wait, what are we\\\\doing here then?",
            target_mode="sassy",
            added_anims=[self.change_students("hesitant", "angry", "sassy")],
            run_time=2
        )
        self.play(self.teacher.change, "tease")
        self.wait(6)
