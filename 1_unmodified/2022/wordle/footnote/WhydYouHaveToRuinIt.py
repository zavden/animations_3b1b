# ==============================================================================
# Scene:      WhydYouHaveToRuinIt
# Source:     videos/_2022/wordle/footnote.py (lines 802-815)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhydYouHaveToRuinIt.py WhydYouHaveToRuinIt -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhydYouHaveToRuinIt(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("Why'd you have to\\\\ruin Wordle!"),
            target_mode="pleading",
            added_anims=[self.teacher.change("guilty")]
        )
        self.play_student_changes("sassy", "angry", "pleading")
        self.wait(3)
        self.teacher_says(
            OldTexText("But ``salet'' is probably\\\\not the best for us"),
            added_anims=[self.change_students("confused", "sassy", "hesitant")]
        )
        self.wait(3)
