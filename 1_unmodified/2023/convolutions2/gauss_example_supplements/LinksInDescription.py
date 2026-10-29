# ==============================================================================
# Scene:      LinksInDescription
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 1145-1163)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LinksInDescription.py LinksInDescription -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LinksInDescription(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.teacher.says("""
                Links for the
                theoretically curious
                in the description
            """),
            self.change_students(
                "pondering", "hooray", "well",
                look_at=self.teacher.eyes
            )
        )
        self.play(self.change_students(
            "pondering", "well", "tease",
            look_at=4 * DOWN,
        ))
        self.wait(5)
