# ==============================================================================
# Scene:      WhoCares
# Source:     videos/_2022/puzzles/subsets.py (lines 845-857)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhoCares.py WhoCares -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhoCares(TeacherStudentsScene):
    def construct(self):
        # Who cares?
        self.play(
            PiCreatureSays(
                self.students[2], "Who cares?", target_mode="angry",
                bubble_config=dict(direction=LEFT),
            ),
            self.teacher.change("guilty"),
            self.students[0].change("sassy"),
            self.students[0].change("hesitant"),
        )
        self.wait(3)
