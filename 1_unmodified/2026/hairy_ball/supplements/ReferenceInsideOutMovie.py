# ==============================================================================
# Scene:      ReferenceInsideOutMovie
# Source:     videos/_2026/hairy_ball/supplements.py (lines 576-600)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceInsideOutMovie.py ReferenceInsideOutMovie -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceInsideOutMovie(TeacherStudentsScene):
    def construct(self):
        # Complain
        morty = self.teacher
        stds = self.students
        self.screen.to_corner(UL)

        self.play(
            stds[0].change("pondering", self.screen),
            stds[1].change("erm", self.screen),
            stds[2].says(
                Text(
                    "Huh? I thought\nyou can turn a\nsphere inside out!",
                    t2s={"can": ITALIC},
                    font_size=42,
                ),
                mode="confused",
                look_at=self.screen,
                bubble_direction=LEFT
            ),
            morty.change("guilty")
        )
        self.wait(2)
        self.play(morty.change('tease'))
        self.wait(3)
