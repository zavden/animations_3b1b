# ==============================================================================
# Scene:      AstuteAmongYou
# Source:     videos/_2022/borwein/supplements.py (lines 37-67)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AstuteAmongYou.py AstuteAmongYou -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AstuteAmongYou(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.play(
            stds[2].says(
                OldTexText("What about\\\\$x=0$?"),
                bubble_direction=LEFT,
                mode="raise_right_hand"
            ),
            stds[0].change("hesitant"),
            stds[1].change("pondering"),
            morty.change("happy", stds[2].eyes),
        )
        self.wait(2)
        self.play(
            stds[0].says("The squeeze theorem!", mode="hooray"),
            RemovePiCreatureBubble(stds[2])
        )
        self.look_at(stds[0].get_corner(UR))
        self.wait(3)

        # Hold Up
        point = stds.get_top() + 2 * UP
        self.play(
            stds[0].debubble(mode="raise_right_hand", look_at=point),
            stds[1].change("thinking", point),
            stds[2].change("erm", point),
            morty.change("tease", point)
        )
        self.wait(5)
