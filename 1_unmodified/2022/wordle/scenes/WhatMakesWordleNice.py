# ==============================================================================
# Scene:      WhatMakesWordleNice
# Source:     videos/_2022/wordle/scenes.py (lines 3183-3192)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatMakesWordleNice.py WhatMakesWordleNice -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatMakesWordleNice(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            OldTexText("This is what makes wordle\\\\such a nice example"),
            added_anims=[self.change_students(
                "pondering", "thinking", "erm",
                look_at=ORIGIN,
            )]
        )
        self.wait(5)
