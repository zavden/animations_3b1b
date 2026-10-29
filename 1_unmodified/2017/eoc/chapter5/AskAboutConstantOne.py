# ==============================================================================
# Scene:      AskAboutConstantOne
# Source:     videos/_2017/eoc/chapter5.py (lines 1070-1100)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutConstantOne.py AskAboutConstantOne -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutConstantOne(TeacherStudentsScene):
    def construct(self):
        note = OldTex(
            "{ d(a^", "t", ")", "\\over \\,", "dt}", 
            "=", "a^", "t", "(\\text{Some constant})"
        )
        note.set_color_by_tex("t", YELLOW)
        note.set_color_by_tex("dt", GREEN)
        note.set_color_by_tex("constant", BLUE)
        note.to_corner(UP+LEFT)
        self.add(note)

        self.student_says(
            "Is there a base where\\\\",
            "that constant is 1?"
        )
        self.play_student_changes(
            "pondering", "raise_right_hand", "thinking",
            # look_at = self.get_students()[1].bubble
        )
        self.wait(2)
        self.play(FadeOut(note[-1], run_time = 3))
        self.wait()

        self.teacher_says(
            "There is!\\\\",
            "$e = 2.71828\\dots$",
            target_mode = "hooray"
        )
        self.play_student_changes(*["confused"]*3)
        self.wait(3)
