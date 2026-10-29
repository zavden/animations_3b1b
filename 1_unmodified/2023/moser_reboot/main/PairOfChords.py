# ==============================================================================
# Scene:      PairOfChords
# Source:     videos/_2023/moser_reboot/main.py (lines 426-435)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PairOfChords.py PairOfChords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PairOfChords(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        self.play(
            self.students[0].change("confused", self.screen),
            self.students[1].says("Pairs of chords?", "raise_left_hand"),
            self.students[2].change("confused", self.screen),
            self.teacher.change("well")
        )
        self.wait(5)
