# ==============================================================================
# Scene:      ComplainAboutGithub
# Source:     videos/_2022/some2/announcement.py (lines 108-123)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplainAboutGithub.py ComplainAboutGithub -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplainAboutGithub(TeacherStudentsScene):
    def construct(self):
        pis = self.students
        morty = self.teacher
        self.play(
            pis[1].says(
                "Aren't GitHub issues\nmeant for, like, tracking\nbugs with code?",
                mode="sassy"
            ),
            morty.change("guilty"),
            pis[0].change("confused"),
            pis[2].change("erm"),
        )
        self.wait(2)
        self.play(morty.change("shruggie"))
        self.wait(2)
