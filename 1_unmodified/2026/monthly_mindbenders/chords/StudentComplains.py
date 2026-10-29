# ==============================================================================
# Scene:      StudentComplains
# Source:     videos/_2026/monthly_mindbenders/chords.py (lines 282-300)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StudentComplains.py StudentComplains -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StudentComplains(TeacherStudentsScene):
    def construct(self):
        # Test
        self.remove(self.background)
        stds = self.students
        morty = self.teacher
        self.play(
            stds[2].says("Hang on, hang on,\nhang on!", mode="angry", bubble_direction=LEFT, run_time=1),
            stds[0].change("erm", stds[2].eyes),
            stds[1].change("guilty", stds[2].eyes),
            morty.change("guilty"),
        )
        self.wait()
        self.play(
            FadeOut(stds[2].bubble),
            stds[2].says("Bertrand's\nParadox!", run_time=1, bubble_direction=LEFT),
            morty.change("tease"),
        )
        self.wait()
