# ==============================================================================
# Scene:      ButSpheresAreSmooth
# Source:     videos/_2021/shadows.py (lines 5830-5842)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ButSpheresAreSmooth.py ButSpheresAreSmooth -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ButSpheresAreSmooth(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("But spheres don't\\\\have flat faces!"),
            target_mode="angry",
            index=2,
            added_anims=[self.teacher.change("guilty")]
        )
        self.play_student_changes(
            "erm", "hesitant", "angry",
            look_at=self.screen,
        )
        self.wait(6)
