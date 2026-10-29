# ==============================================================================
# Scene:      WhySlowAtAll
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 241-253)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhySlowAtAll.py WhySlowAtAll -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhySlowAtAll(TeacherStudentsScene):
    def construct(self):
        # Test
        stds = self.students
        self.play(
            stds[0].change("pondering", self.screen),
            stds[1].says("Why would light\nslow down at all?", mode="confused", bubble_direction=LEFT, look_at=self.screen),
            stds[2].change("erm", self.screen),
            self.teacher.change("tease"),
        )
        self.wait(2)
        self.play(self.change_students("hesitant", "maybe", "pondering", look_at=self.screen))
        self.wait(3)
