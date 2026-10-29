# ==============================================================================
# Scene:      ReferenceComplexExponents
# Source:     videos/_2025/laplace/main_supplements.py (lines 125-154)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceComplexExponents.py ReferenceComplexExponents -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceComplexExponents(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        for pi in self.pi_creatures:
            pi.body.insert_n_curves(500)

        self.play(
            morty.change("raise_right_hand"),
            self.change_students('pondering', 'thinking', 'tease', look_at=self.screen)
        )
        self.wait(3)
        self.play(self.change_students('tease', 'tease', 'confused', look_at=self.screen))
        self.wait(2)
        self.play(self.change_students('thinking', 'tease', 'erm', look_at=self.screen))
        self.wait(2)
        self.play(
            morty.change('hesitant', stds[2].eyes),
            stds[2].says("Why?", mode='maybe', bubble_direction=LEFT),
        )
        self.wait(3)
        self.play(
            morty.change("raise_right_hand"),
            stds[2].debubble(mode="pondering", look_at=3 * UR),
            stds[0].change("pondering", look_at=3 * UR),
            stds[1].change("hesitant", look_at=3 * UR),
        )
        self.wait(3)
