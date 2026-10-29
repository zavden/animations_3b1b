# ==============================================================================
# Scene:      Given2DThinkComplex
# Source:     videos/_2017/leibniz.py (lines 1318-1343)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Given2DThinkComplex.py Given2DThinkComplex -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Given2DThinkComplex(TeacherStudentsScene):
    def construct(self):
        tex = OldTexText("2D $\\Leftrightarrow$ Complex numbers")
        plane = ComplexPlane(
            x_radius = 0.6*FRAME_X_RADIUS,
            y_radius = 0.6*FRAME_Y_RADIUS,
        )
        plane.add_coordinates()
        plane.set_height(FRAME_Y_RADIUS)
        plane.to_corner(UP+LEFT)

        self.teacher_says(tex)
        self.play_student_changes("pondering", "confused", "erm")
        self.wait()
        self.play(
            Write(plane),
            RemovePiCreatureBubble(
                self.teacher,
                target_mode = "raise_right_hand"
            )
        )
        self.play_student_changes(
            *["thinking"]*3,
            look_at = plane
        )
        self.wait(3)
