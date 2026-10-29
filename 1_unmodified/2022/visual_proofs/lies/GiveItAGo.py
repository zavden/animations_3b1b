# ==============================================================================
# Scene:      GiveItAGo
# Source:     videos/_2022/visual_proofs/lies.py (lines 1271-1285)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GiveItAGo.py GiveItAGo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GiveItAGo(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        ss = self.students

        self.play(
            morty.says("Can you see\nwhat's happening?"),
            ss[0].change("pondering", self.screen),
            ss[1].change("angry", self.screen),
            ss[2].change("confused", self.screen),
        )
        self.wait()
        self.play(ss[1].change("maybe"))
        self.play(morty.change("tease"), ss[0].change("thinking"))
        self.wait(4)
