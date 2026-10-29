# ==============================================================================
# Scene:      ReferenceZSquared
# Source:     videos/_2026/print_gallery/supplements.py (lines 460-476)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceZSquared.py ReferenceZSquared -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceZSquared(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change("raise_right_hand"),
            self.change_students("pondering", "thinking", "pondering", look_at=self.screen)
        )
        self.wait(2)
        self.look_at(3 * UP, run_time=3)
        self.play(
            self.change_students("erm", "hesitant", "maybe", look_at=3 * UR),
            morty.change("tease"),
        )
        self.wait(5)
