# ==============================================================================
# Scene:      TransitionTo3b1bTalent
# Source:     videos/_2026/print_gallery/supplements.py (lines 587-610)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TransitionTo3b1bTalent.py TransitionTo3b1bTalent -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TransitionTo3b1bTalent(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(1000)

        words = Text("3b1b Talent")
        words.move_to(self.hold_up_spot, DOWN)

        self.play(
            self.change_students("confused", "tired", "concentrating", look_at=2 * UP),
            morty.change("tease")
        )
        self.wait(3)
        self.play(self.change_students("maybe", "erm", "tired"))
        self.wait(2)
        self.play(
            morty.change("raise_right_hand"),
            FadeIn(words, UP),
            self.change_students("pondering", "pondering", "pondering", look_at=morty.eyes),
        )
        self.wait(3)
