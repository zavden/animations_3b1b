# ==============================================================================
# Scene:      HowIsThisHelpful
# Source:     videos/_2024/holograms/supplements.py (lines 477-492)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowIsThisHelpful.py HowIsThisHelpful -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowIsThisHelpful(TeacherStudentsScene):
    def construct(self):
        # Test
        stds = self.students
        morty = self.teacher
        self.play(LaggedStart(
            stds[1].says("What does this have\nto do with recording 3d?", mode="maybe", look_at=self.screen),
            stds[0].change("confused", self.screen),
            stds[2].change("erm", self.screen),
            lag_ratio=0.25,
            run_time=2
        ))
        self.play(morty.change('well'))
        self.wait(2)
        self.play(self.change_students("maybe", "confused", "pondering", look_at=self.screen))
        self.wait(5)
