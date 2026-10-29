# ==============================================================================
# Scene:      LightDoesntHaveTreads
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 203-213)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LightDoesntHaveTreads.py LightDoesntHaveTreads -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LightDoesntHaveTreads(TeacherStudentsScene):
    def construct(self):
        # Test
        stds = self.students
        self.play(
            stds[0].change("confused", self.screen),
            stds[1].change("erm", self.screen),
            stds[2].says("But, light doesn't\nhave treads...", mode="sassy", bubble_direction=LEFT),
            self.teacher.change("guilty"),
        )
        self.wait(4)
