# ==============================================================================
# Scene:      WhyDoesAddingCauseAShift
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 553-574)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyDoesAddingCauseAShift.py WhyDoesAddingCauseAShift -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyDoesAddingCauseAShift(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            stds[2].says("But, why?", look_at=morty.eyes, mode="raise_left_hand", bubble_direction=LEFT),
            self.change_students("pondering", "pondering", look_at=self.screen),
            morty.change("guilty", self.screen),
        )
        self.wait()
        self.play(stds[2].change("confused", self.screen))
        self.wait(2)
        self.play(morty.change("tease", stds[2].eyes))
        self.wait()
        self.play(
            morty.change("raise_right_hand", 3 * UR),
            stds[2].debubble(look_at=3 * UR),
            self.change_students("erm", "hesitant", look_at=3 * UR)
        )
        self.wait(3)
