# ==============================================================================
# Scene:      ComplainAboutRuleChange
# Source:     videos/_2020/beta/beta2.py (lines 1538-1552)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplainAboutRuleChange.py ComplainAboutRuleChange -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplainAboutRuleChange(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Wait, the rules\\\\changed?",
            target_mode="sassy",
            added_anims=[self.teacher.change, "tease"]
        )
        self.play_student_changes("erm", "confused")
        self.wait(4)
        self.teacher_says("You may enjoy\\\\``Measure theory''")
        self.play_all_student_changes(
            "pondering",
            look_at=self.teacher.bubble
        )
        self.wait(8)
