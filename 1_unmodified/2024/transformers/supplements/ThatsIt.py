# ==============================================================================
# Scene:      ThatsIt
# Source:     videos/_2024/transformers/supplements.py (lines 1792-1806)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThatsIt.py ThatsIt -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThatsIt(TeacherStudentsScene):
    def construct(self):
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)
        self.play(
            self.teacher.says("That's it!", mode="hooray", look_at=self.students),
            self.change_students("happy", "thinking", "well", look_at=self.screen)
        )
        self.wait()
        self.play(self.teacher.debubble(mode="raise_right_hand", look_at=self.screen))
        self.wait()
        self.play(
            self.change_students("thinking", "tease", "happy", look_at=self.screen)
        )
        self.wait(3)
