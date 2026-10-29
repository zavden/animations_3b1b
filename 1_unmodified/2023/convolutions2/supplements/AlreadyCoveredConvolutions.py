# ==============================================================================
# Scene:      AlreadyCoveredConvolutions
# Source:     videos/_2023/convolutions2/supplements.py (lines 81-169)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AlreadyCoveredConvolutions.py AlreadyCoveredConvolutions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AlreadyCoveredConvolutions(TeacherStudentsScene):
    def construct(self):
        # Ask
        morty = self.teacher
        stds = self.students
        self.screen.to_edge(UR)
        self.play(
            stds[2].says(
                "Wait, didn't you already\ncover convolutions?",
                mode="dance_1"
            ),
            morty.change("guilty"),
        )
        self.play(
            self.change_students("hesitant", "awe", None, look_at=self.screen)
        )
        self.wait(2)

        # Show video
        words = VGroup(
            Text("Only discrete examples", font_size=48),
            Text(
                """
                Probability
                Moving averages
                Image processing
                Polynomial multiplication
                Relationship with FFTs
                """,
                alignment="LEFT",
                font_size=36
            ),
        )
        words.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        words[1].shift(0.25 * RIGHT)
        words.to_corner(UL)
        words.to_edge(UP)

        self.play(LaggedStart(
            morty.change("raise_right_hand", look_at=self.screen),
            stds[2].debubble(mode="sassy", look_at=self.screen),
            stds[1].change("pondering", look_at=self.screen),
        ))
        self.wait(2)
        self.play(
            Write(words[0], run_time=1),
            self.change_students("pondering", "tease", "plain", look_at=words)
        )
        self.wait(3)
        self.play(FadeIn(words[1], run_time=1, lag_ratio=0.1))
        self.wait(3)

        # Awkward spot
        no_prereq = Text("Not a \n prerequisite", font_size=60)
        no_prereq.move_to(words).to_edge(LEFT, buff=1.0)
        no_prereq.set_color(RED)
        redundancy_words = Text("But some overlap\nwith this video")
        redundancy_words.move_to(no_prereq, LEFT)
        redundancy_words.match_color(no_prereq)
        arrow = Vector(2.5 * RIGHT)
        arrow.next_to(no_prereq, RIGHT)
        arrow.match_color(no_prereq)

        self.play(
            morty.change("guilty"),
            self.change_students("hesitant", "pondering", "hesitant", look_at=morty.eyes)
        )
        self.wait()
        self.look_at(no_prereq, added_anims=[
            FadeOut(words, LEFT),
            FadeIn(no_prereq, LEFT),
        ])
        self.play(
            GrowArrow(arrow),
            morty.change("raise_left_hand", self.screen)
        )
        self.wait(2)
        self.play(morty.change("maybe"))
        self.look_at(no_prereq, added_anims=[
            FadeOut(no_prereq, UP),
            FadeIn(redundancy_words, UP),
            arrow.animate.stretch(0.8, 0, about_edge=RIGHT),
        ])
        self.wait(3)
        self.play(
            morty.change("tease"),
            self.change_students("happy", "thinking", "happy", look_at=morty.eyes),
        )
        self.wait(4)
