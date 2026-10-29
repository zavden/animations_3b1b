# ==============================================================================
# Scene:      NonPlanarComplaint
# Source:     videos/_2023/moser_reboot/main.py (lines 984-1001)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NonPlanarComplaint.py NonPlanarComplaint -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NonPlanarComplaint(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        morty = self.teacher
        self.remove(self.background)

        self.play(
            stds[2].says("But our graph\nis not planar!", mode="angry"),
            stds[1].change("sassy", 3 * UR),
            stds[0].change("hesitant", 3 * UR),
            morty.change("tease"),
        )
        self.wait(3)
        self.play(
            morty.change("raise_left_hand"),
            self.change_students("angry", "sassy", "hesitant")
        )
        self.wait(4)
