# ==============================================================================
# Scene:      OnDumbJoke
# Source:     videos/_2023/moser_reboot/main.py (lines 948-965)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OnDumbJoke.py OnDumbJoke -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OnDumbJoke(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change("raise_left_hand", 3 * UR),
            self.change_students("hesitant", "happy", "tease", look_at=3 * UR)
        )
        self.wait(3)
        self.play(
            stds[0].says("Um, no, Euler was\na person...", mode="sassy"),
            stds[1].change("hesitant", stds[0].eyes),
            stds[2].change("jamming", stds[0].eyes),
            morty.change("well", stds[0].eyes)
        )
        self.wait(4)
