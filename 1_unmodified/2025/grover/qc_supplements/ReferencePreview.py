# ==============================================================================
# Scene:      ReferencePreview
# Source:     videos/_2025/grover/qc_supplements.py (lines 791-818)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferencePreview.py ReferencePreview -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferencePreview(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(1000)

        self.play(
            morty.says("First, a preview"),
            self.change_students("happy", "tease", "happy", look_at=morty.eyes)
        )
        self.wait(4)
        self.play(
            morty.debubble(mode="raise_right_hand"),
            self.change_students("pondering", "thinking", "pondering", look_at=2 * UR)
        )
        self.look_at(3 * UR)
        self.wait(4)

        # Ask about sign
        stds = self.students
        self.play(
            stds[2].says("Why can you flip the\nkey sign like that?", mode="raise_left_hand", look_at=self.teacher.eyes),
            stds[1].change("sassy", look_at=3 * UR),
            stds[0].change("maybe", look_at=3 * UR),
            morty.change('tease')
        )
        self.wait(5)
