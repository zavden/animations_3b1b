# ==============================================================================
# Scene:      UnsatisfyingEnd
# Source:     videos/_2022/borwein/supplements.py (lines 587-607)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnsatisfyingEnd.py UnsatisfyingEnd -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UnsatisfyingEnd(TeacherStudentsScene):
    def construct(self):
        # Ask
        self.remove(self.background)
        morty = self.teacher
        stds = self.students

        self.play(
            stds[0].says("But you haven't explained\nwhy any of that is true?", mode="angry"),
            stds[1].change("hesitant"),
            stds[2].change("pleading"),
            morty.change("guilty"),
        )
        stds[0].bubble.insert_n_curves(20)
        self.wait(3)
        self.play(
            morty.says("Patience.", mode="tease"),
            stds[0].debubble(),
            stds[2].change("hesitant")
        )
        self.wait(2)
