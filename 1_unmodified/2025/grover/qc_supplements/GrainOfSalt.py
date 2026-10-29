# ==============================================================================
# Scene:      GrainOfSalt
# Source:     videos/_2025/grover/qc_supplements.py (lines 1365-1393)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GrainOfSalt.py GrainOfSalt -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GrainOfSalt(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)

        self.play(
            morty.change("coin_flip_2"),
            self.change_students("hesitant", "sassy", "tease", look_at=self.screen),
        )
        self.wait(2)
        self.play(
            morty.says("Take this with\na grain of salt", mode="hesitant"),
            self.change_students("pondering", "pondering", "pondering", look_at=morty.eyes),
        )
        self.wait(3)
        self.play(
            morty.debubble(mode="raise_right_hand", look_at=3 * UP),
            self.change_students("hesitant", "erm", "hesitant", look_at=2 * UP)
        )
        self.wait(4)

        # More pondering
        self.play(
            morty.change("tease"),
            self.change_students("pondering", "thinking", "thinking", look_at=2 * UP)
        )
        self.wait(5)
