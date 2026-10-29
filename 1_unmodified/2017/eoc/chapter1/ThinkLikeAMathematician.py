# ==============================================================================
# Scene:      ThinkLikeAMathematician
# Source:     videos/_2017/eoc/chapter1.py (lines 1524-1546)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThinkLikeAMathematician.py ThinkLikeAMathematician -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThinkLikeAMathematician(TeacherStudentsScene):
    def construct(self):
        pi_R_squraed = OldTex("\\pi", "R", "^2")
        pi_R_squraed.set_color_by_tex("R", YELLOW)
        pi_R_squraed.move_to(self.get_students(), UP)
        pi_R_squraed.set_fill(opacity = 0)

        self.play(
            pi_R_squraed.shift, 2*UP,
            pi_R_squraed.set_fill, None, 1
        )
        self.play_student_changes(*["hooray"]*3)
        self.wait(2)
        self.play_student_changes(
            *["pondering"]*3,
            look_at = self.teacher.eyes,
            added_anims = [PiCreatureSays(
                self.teacher, "But why did \\\\ that work?"
            )]
        )
        self.play(FadeOut(pi_R_squraed))
        self.look_at(2*UP+4*LEFT)
        self.wait(5)
