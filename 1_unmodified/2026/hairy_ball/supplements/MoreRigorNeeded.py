# ==============================================================================
# Scene:      MoreRigorNeeded
# Source:     videos/_2026/hairy_ball/supplements.py (lines 833-853)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoreRigorNeeded.py MoreRigorNeeded -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoreRigorNeeded(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher

        words = Text("More rigor\nneeded", font_size=60)
        arrow = Vector(1.5 * LEFT, thickness=8)
        label = VGroup(arrow, words)
        label.arrange(RIGHT, SMALL_BUFF)
        label.next_to(self.screen, RIGHT)

        self.add(words)
        self.play(
            morty.change("hesitant"),
            self.change_students("confused", "sassy", "erm", look_at=self.screen),
            Write(words),
        )
        self.play(
            GrowArrow(arrow)
        )
        self.wait(4)
