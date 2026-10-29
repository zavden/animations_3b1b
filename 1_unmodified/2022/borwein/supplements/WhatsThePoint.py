# ==============================================================================
# Scene:      WhatsThePoint
# Source:     videos/_2022/borwein/supplements.py (lines 132-152)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatsThePoint.py WhatsThePoint -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatsThePoint(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        self.play(
            stds[2].says(
                OldTexText(R"So it computes $\pi$ \\ what's the point?"),
                bubble_direction=LEFT,
                mode="angry",
            ),
            stds[1].change("sassy", self.screen),
            stds[0].change("pondering", self.screen),
            self.teacher.change("guilty")
        )
        self.wait(2)
        self.play(
            self.teacher.says("Look what \n happens next", mode="tease", bubble_direction=RIGHT),
            stds[2].debubble(),
            stds[1].change("erm"),
            stds[0].change("thinking"),
        )
        self.wait(2)
