# ==============================================================================
# Scene:      WhatsGoingOn
# Source:     videos/_2021/newton_fractal.py (lines 3232-3248)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatsGoingOn.py WhatsGoingOn -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatsGoingOn(TeacherStudentsScene):
    def construct(self):
        self.screen.set_height(4, about_edge=UL)
        self.screen.set_fill(BLACK, 1)
        self.add(self.screen)

        self.student_says(
            "What the %$!* is\ngoing on?",
            target_mode="angry",
            look_at=self.screen,
            index=2,
            added_anims=[LaggedStart(*(
                pi.change("guilty", self.students[2].eyes)
                for pi in [self.teacher, *self.students[:2]]
            ), run_time=2)]
        )
        self.wait(4)
