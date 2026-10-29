# ==============================================================================
# Scene:      AskAboutPosition
# Source:     videos/_2023/moser_reboot/main.py (lines 126-138)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutPosition.py AskAboutPosition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutPosition(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.remove(self.background)

        self.play(LaggedStart(
            stds[1].says("Doesn't it depend on\nwhere the points are?", mode="sassy"),
            stds[0].change('confused', self.screen),
            stds[2].change('pondering', self.screen),
            morty.change("guilty", stds[1].eyes)
        ))
        self.wait(5)
