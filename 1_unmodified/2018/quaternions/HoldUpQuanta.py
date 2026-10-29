# ==============================================================================
# Scene:      HoldUpQuanta
# Source:     videos/_2018/quaternions.py (lines 6129-6149)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HoldUpQuanta.py HoldUpQuanta -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HoldUpQuanta(TeacherStudentsScene):
    def construct(self):
        logo = ImageMobject("Quanta logo")
        logo.set_width(6)
        logo.next_to(self.teacher, UR)
        logo.to_edge(RIGHT, buff=2)

        words = OldTexText("Associated quaternion post")
        words.to_edge(UP, buff=LARGE_BUFF)
        arrow = Arrow(logo.get_top(), words.get_bottom())

        self.play(
            FadeInFromDown(logo),
            self.teacher.change, "raise_right_hand"
        )
        self.play_all_student_changes("hooray")
        self.play(
            GrowArrow(arrow),
            GrowFromPoint(words, arrow.get_start())
        )
        self.wait(3)
