# ==============================================================================
# Scene:      Intro
# Source:     videos/_2022/visual_proofs/lies.py (lines 115-131)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Intro.py Intro -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Intro(TeacherStudentsScene):
    CONFIG = {"background_color": BLACK}

    def construct(self):
        morty = self.teacher
        ss = self.students

        self.play(morty.change("raise_right_hand"))
        self.play_student_changes(
            "pondering", "angry", "confused",
            look_at=self.screen
        )
        self.wait()
        self.play(ss[0].change("worried", self.screen))
        self.wait()
        self.play(ss[1].change("pondering", self.screen))
        self.wait(3)
