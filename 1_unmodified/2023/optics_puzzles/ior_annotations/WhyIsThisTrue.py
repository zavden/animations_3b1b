# ==============================================================================
# Scene:      WhyIsThisTrue
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1189-1206)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyIsThisTrue.py WhyIsThisTrue -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyIsThisTrue(TeacherStudentsScene):
    def construct(self):
        # Test
        stds = self.students
        morty = self.teacher
        self.screen.to_corner(UR)
        self.play(
            stds[2].says("Why is it\na phase shift?", look_at=self.screen),
            stds[1].change("confused", self.screen),
            stds[0].change("pondering", self.screen),
            morty.change("guilty", stds[0].eyes)
        )
        self.wait(2)
        self.play(
            self.change_students("pondering", "pleading", "maybe", look_at=self.screen),
            morty.change("hesitant", self.screen)
        )
        self.wait(3)
