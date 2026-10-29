# ==============================================================================
# Scene:      WhyThePowersOfTwo
# Source:     videos/_2023/moser_reboot/main.py (lines 1180-1192)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyThePowersOfTwo.py WhyThePowersOfTwo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyThePowersOfTwo(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        morty = self.teacher
        self.remove(self.background)

        self.play(LaggedStart(
            stds[0].change("confused", self.screen),
            stds[1].says("Why the powers \n of 2?"),
            stds[2].change("pondering", self.screen),
            morty.change("tease")
        ))
        self.wait(6)
