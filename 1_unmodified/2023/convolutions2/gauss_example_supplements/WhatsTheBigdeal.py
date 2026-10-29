# ==============================================================================
# Scene:      WhatsTheBigdeal
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 976-1045)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatsTheBigdeal.py WhatsTheBigdeal -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhatsTheBigdeal(TeacherStudentsScene):
    def construct(self):
        # What's the big deal
        morty = self.teacher
        stds = self.students
        self.remove(self.background)

        self.play(
            stds[0].change("pondering", look_at=self.screen),
            stds[1].change("maybe", look_at=self.screen),
            stds[2].says("What's the\nbig deal?", mode="dance_3"),
            morty.change("guilty"),
        )
        self.wait(2)
        self.play(
            self.change_students("pondering", "sassy", "hesitant", look_at=self.screen),
            morty.change("plain"),
            run_time=2
        )
        self.wait(6)

        # Aren't they common
        self.play(
            stds[2].debubble(mode="heistant"),
            stds[1].says("What else\nwould it be?", mode="maybe", run_time=1),
            stds[0].change("well"),
        )
        self.play(
            stds[2].says("Normal distributions\nare very common\nright?", mode="speaking", look_at=morty.eyes),
            run_time=2,
        )
        self.add(stds[2].bubble, stds[2].bubble.content)
        self.wait(3)

        # But are they?
        common_words = stds[2].bubble.content["Normal distributions\nare very common"][0].copy()
        are_they = Text("But are they?")
        are_they.set_color(RED)
        are_they.move_to(self.hold_up_spot, DOWN)

        self.play(
            stds[0].change("pondering", look_at=self.screen),
            stds[1].debubble(),
            stds[2].debubble(),
            morty.change("sassy"),
            FadeIn(are_they, UP),
            common_words.animate.next_to(are_they, UP)
        )
        self.wait()
        self.play(morty.change("hesitant", are_they))
        self.wait(2)

        # Central limit theorem
        clt = Text("Central Limit Theorem")
        clt.set_color(YELLOW)
        clt.move_to(common_words).to_edge(UP, buff=LARGE_BUFF)
        implies = Tex(R"\Downarrow")
        implies.next_to(clt, DOWN)

        n = len("Normaldistributions")
        self.play(
            morty.change("raise_right_hand"),
            self.change_students("pondering", "erm", "pondering", look_at=clt),
            common_words[:n].animate.next_to(implies, DOWN),
            FadeOut(common_words[n:], DOWN),
            FadeOut(are_they, DOWN),
            Write(clt),
            Write(implies)
        )
        self.wait(5)
