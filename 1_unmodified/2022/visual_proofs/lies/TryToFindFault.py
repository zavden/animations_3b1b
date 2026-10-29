# ==============================================================================
# Scene:      TryToFindFault
# Source:     videos/_2022/visual_proofs/lies.py (lines 2127-2154)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TryToFindFault.py TryToFindFault -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TryToFindFault(TeacherStudentsScene):
    def construct(self):
        # Setup
        morty = self.teacher
        ss = self.students

        points = compass_directions(5, start_vect=UP)
        star = Polygon(*(points[i] for i in [0, 2, 4, 1, 3]))
        star.set_fill(YELLOW, 1)
        star.set_stroke(width=0)
        star.set_gloss(1)
        star.set_height(0.5)
        stars = star.replicate(3)
        stars.arrange(RIGHT)
        stars.move_to(self.hold_up_spot, DOWN)
        stars.insert_n_curves(10)

        self.play(
            morty.says("I dare you to\nfind a fault", mode="tease"),
        )
        self.play_student_changes("pondering", "pondering", "sassy")
        self.wait()
        self.play(
            morty.debubble(mode="raise_right_hand"),
            self.change_students("thinking", "happy", "tease"),
            Write(stars)
        )
        self.wait(3)
