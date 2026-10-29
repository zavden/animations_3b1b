# ==============================================================================
# Scene:      AskAboutHigherOrderBeams
# Source:     videos/_2024/holograms/supplements.py (lines 959-971)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutHigherOrderBeams.py AskAboutHigherOrderBeams -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutHigherOrderBeams(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        morty = self.teacher
        self.play(LaggedStart(
            stds[0].change('pondering', self.screen),
            stds[1].says("What about higher\norder beams?", look_at=self.screen),
            stds[2].change("confused", self.screen),
            morty.change("tease")
        ))
        self.wait()
        self.play(stds[1].change("sassy", morty.eyes))
        self.wait(6)
