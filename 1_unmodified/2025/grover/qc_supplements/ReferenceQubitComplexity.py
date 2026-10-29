# ==============================================================================
# Scene:      ReferenceQubitComplexity
# Source:     videos/_2025/grover/qc_supplements.py (lines 517-534)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceQubitComplexity.py ReferenceQubitComplexity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceQubitComplexity(TeacherStudentsScene):
    def construct(self):
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(1000)
        expr = Tex(R"\mathds{R}^2 \text{ vs. } \mathds{C}^2", font_size=60)
        expr.move_to(self.hold_up_spot, DOWN)
        self.play(
            self.teacher.change("raise_right_hand"),
            self.change_students("erm", "confused", "tease", look_at=expr),
            FadeIn(expr, UP)
        )
        self.wait(2)
        self.play(
            self.teacher.change("tease"),
            FadeOut(expr, shift=3 * RIGHT, path_arc=-90 * DEG),
            self.change_students("pondering", "pondering", "pondering", look_at=self.screen)
        )
        self.wait(4)
