# ==============================================================================
# Scene:      ValueInSharedGoals
# Source:     videos/_2022/some2/winners.py (lines 452-500)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ValueInSharedGoals.py ValueInSharedGoals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ValueInSharedGoals(TeacherStudentsScene):
    def construct(self):
        # Start
        morty = self.teacher

        self.play(
            morty.says("Never underestimate\ncommunity and\ndeadlines"),
            self.change_students("happy", "tease", "thinking"),
        )
        self.wait(5)

        self.play(
            morty.debubble(mode="raise_right_hand", look_at=self.screen),
            self.change_students("pondering", "thinking", "erm", look_at=self.screen),
        )
        self.wait(2)

        # Show links
        links = VGroup(
            Text("explanaria.github.io/crystalgroups"),
            Text("thenumb.at/Autodiff"),
            Text("xperimex.com/blog/panorama-homography"),
            Text("calmcode.io/blog/inverse-turing-test.html"),
            Text("summbit.com/blog/bezier-curve-guide"),
            Text("lukelavalva.com/theoryofsliding"),
            Text("chessengines.org"),
            OldTex("\\vdots")
        )
        links.arrange(DOWN, aligned_edge=LEFT)
        links[-1].match_x(links[-2])
        links.set_width(5)
        links.to_corner(UR)
        self.play(
            morty.change("raise_left_hand", links),
            self.change_students("tease", "happy", "thinking", look_at=links),
            FadeIn(links, lag_ratio=0.3, run_time=2)
        )
        self.wait(4)

        # Who won
        stds = self.students
        self.play(
            FadeOut(links, RIGHT),
            morty.change("guilty"),
            stds[0].says("But, like, who actually\nwon the contest?"),
            stds[1].change("erm", stds[0].eyes),
            stds[2].change("sassy", stds[0].eyes),
        )
        self.wait(3)
