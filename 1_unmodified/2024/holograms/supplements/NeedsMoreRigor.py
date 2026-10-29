# ==============================================================================
# Scene:      NeedsMoreRigor
# Source:     videos/_2024/holograms/supplements.py (lines 1101-1118)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NeedsMoreRigor.py NeedsMoreRigor -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NeedsMoreRigor(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher

        arrow = Vector(LEFT, thickness=4)
        arrow.move_to(2.5 * UP)
        words = Text("Sketchy and non-rigorous")
        words.next_to(arrow)

        self.play(
            morty.change("guilty"),
            self.change_students("erm", "hesitant", "sassy", look_at=self.screen)
        )
        self.play(
            GrowArrow(arrow),
            Write(words)
        )
        self.wait(4)
