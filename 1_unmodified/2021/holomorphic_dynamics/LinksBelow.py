# ==============================================================================
# Scene:      LinksBelow
# Source:     videos/_2021/holomorphic_dynamics.py (lines 3430-3440)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LinksBelow.py LinksBelow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LinksBelow(TeacherStudentsScene):
    def construct(self):
        self.pi_creatures.flip().flip()
        self.teacher_says("Links below")
        self.play_student_changes(
            "pondering", "thinking", "pondering",
            look_at=FRAME_HEIGHT * DOWN,
        )
        self.wait(2)
        self.play(self.teacher.change("happy"))
        self.wait(4)
