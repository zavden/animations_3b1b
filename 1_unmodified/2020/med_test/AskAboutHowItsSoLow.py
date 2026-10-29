# ==============================================================================
# Scene:      AskAboutHowItsSoLow
# Source:     videos/_2020/med_test.py (lines 5677-5699)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutHowItsSoLow.py AskAboutHowItsSoLow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutHowItsSoLow(TeacherStudentsScene):
    def construct(self):
        question = OldTexText(
            "How can it be 1 in 11\\\\"
            "if the test is accurate more\\\\"
            "than 90\\% of the time?",
            tex_to_color_map={
                "1 in 11": BLUE,
                "90\\%": YELLOW,
            }
        )
        self.student_says(
            question,
            index=1,
            target_mode="maybe",
        )
        self.play_student_changes(
            "confused", "maybe", "confused",
            look_at=question,
        )
        self.wait()
        self.play(self.teacher.change, "tease", question)
        self.wait(2)
