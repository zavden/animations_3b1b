# ==============================================================================
# Scene:      EnthusiasticAboutRunTime
# Source:     videos/_2022/convolutions/supplements.py (lines 485-500)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EnthusiasticAboutRunTime.py EnthusiasticAboutRunTime -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class EnthusiasticAboutRunTime(TeacherStudentsScene):
    def construct(self):
        run_time = OldTex(R"\mathcal{O}\big(N \log(N)\big)")
        run_time.move_to(self.hold_up_spot, DOWN)
        self.play(
            self.teacher.change("raise_right_hand"),
            FadeIn(run_time, UP),
            self.change_students("thinking", "tease", "happy", look_at=run_time),
        )
        self.wait(2)
        self.play(
            self.teacher.says("That feels\nlike magic!", mode="hooray"),
            run_time.animate.to_edge(UP),
            self.change_students("tease", "happy", "tease")
        )
        self.wait(3)
