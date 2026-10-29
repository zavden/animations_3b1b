# ==============================================================================
# Scene:      DejaVu
# Source:     videos/_2024/holograms/supplements.py (lines 897-917)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DejaVu.py DejaVu -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DejaVu(TeacherStudentsScene):
    def construct(self):
        # Test
        stds = self.students
        self.play(
            stds[0].change("pondering", self.screen),
            stds[1].change("pondering", self.screen),
            stds[2].says("That looks\nfamiliar", bubble_config=dict(direction=LEFT), look_at=self.screen),
            self.teacher.change("tease"),
        )
        self.wait(2)

        diff_eq = Tex(R"d \cdot \sin(\theta) = \lambda")
        diff_eq.next_to(stds[0], UR)
        self.play(
            stds[1].change("raise_left_hand", look_at=diff_eq),
            FadeIn(diff_eq, UP)
        )
        self.look_at(diff_eq)
        self.play(stds[2].change("pondering", diff_eq))
        self.wait(3)
