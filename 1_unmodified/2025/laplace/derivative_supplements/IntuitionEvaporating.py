# ==============================================================================
# Scene:      IntuitionEvaporating
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 580-610)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntuitionEvaporating.py IntuitionEvaporating -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntuitionEvaporating(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(1000)

        words = Text("Intuition", font_size=36).replicate(12)
        words.move_to(stds.get_top() + 0.5 * DOWN)
        for word in words:
            word.shift(random.uniform(-4, 4) * RIGHT)

        self.play(
            morty.change("raise_right_hand"),
            self.change_students("pondering", "pondering", "pondering", look_at=self.screen),
        )
        self.wait()
        y0 = words.get_y()
        self.play(
            self.change_students("tired", "tired", "tired", look_at=self.screen),
            morty.change("guilty"),
            LaggedStart(
                *(
                    UpdateFromAlphaFunc(word, lambda m, a: m.set_y(y0 + 2 * a).set_fill(opacity=there_and_back(a)))
                    for word in words
                ),
                lag_ratio=0.1,
                run_time=6
            ),
        )
