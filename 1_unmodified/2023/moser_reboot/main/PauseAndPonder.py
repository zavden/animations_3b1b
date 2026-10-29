# ==============================================================================
# Scene:      PauseAndPonder
# Source:     videos/_2023/moser_reboot/main.py (lines 438-447)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PauseAndPonder.py PauseAndPonder -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PauseAndPonder(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        self.play(LaggedStart(
            self.students[0].change("pondering", self.screen),
            self.students[1].change("thinking", self.screen),
            self.students[2].change("erm", self.screen),
            self.teacher.says("Pause and\nponder", mode="hooray")
        ))
        self.wait(5)
