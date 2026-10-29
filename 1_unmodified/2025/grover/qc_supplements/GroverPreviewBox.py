# ==============================================================================
# Scene:      GroverPreviewBox
# Source:     videos/_2025/grover/qc_supplements.py (lines 821-841)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GroverPreviewBox.py GroverPreviewBox -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GroverPreviewBox(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        rect = ScreenRectangle(height=4.0)
        rect.next_to(morty, UL)
        rect.set_fill(BLACK, 1).set_stroke(WHITE, 2)

        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)
        for pi in self.students:
            pi.change_mode("confused").look_at(rect)

        self.add(rect)
        self.play(
            morty.change("raise_right_hand", rect),
            self.change_students("pondering", "pondering", "pondering", look_at=rect)
        )
        self.wait(4)
        self.play(self.change_students("tease", "thinking", "pondering", look_at=rect))
        self.wait(5)
