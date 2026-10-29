# ==============================================================================
# Scene:      ReferenceZetaPromise
# Source:     videos/_2022/puzzles/subsets.py (lines 5345-5366)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceZetaPromise.py ReferenceZetaPromise -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceZetaPromise(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        ss = self.students
        self.student_says(
            OldTexText("Didn't you once promise\\\\a video about $\\zeta(s)$ and primes?"),
            target_mode="sassy",
            index=0,
            added_anims=[
                ss[1].change("hesitant"),
                ss[2].change("angry"),
            ]
        )
        self.play(morty.change("guilty"))
        self.wait(3)
        self.play(
            RemovePiCreatureBubble(ss[0], target_mode="pondering", look_at=self.screen),
            ss[1].change("pondering", self.screen),
            ss[2].change("thinking", self.screen),
            morty.change("raise_right_hand", self.screen)
        )
        self.wait(4)
