# ==============================================================================
# Scene:      DumbIdea
# Source:     videos/_2022/convolutions/supplements.py (lines 387-460)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DumbIdea.py DumbIdea -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DumbIdea(TeacherStudentsScene):
    def construct(self):
        # Bad idea
        morty = self.teacher
        stds = self.students
        self.play(
            morty.change("happy", look_at=self.screen),
            self.change_students("pondering", "pondering", "frustrated", look_at=self.screen)
        )
        self.wait()
        self.student_says("Uh...", target_mode="hesitant", bubble_direction=LEFT, index=2)
        self.play(Blink(stds[2]))
        self.student_says(
            "That's idiotic!", target_mode="angry", index=2,
            added_anims=[morty.change("guilty"), stds[1].change("erm")]
        )
        self.wait(2)

        # Samples
        self.student_says(
            OldTexText(R"Calculating the samples\\is already $\mathcal{O}(N^2)$"),
            target_mode="concentrating",
            look_at=self.screen,
            added_anims=[stds[0].change("erm"), stds[1].change("hesitant")]
        )
        self.wait(5)
        self.student_says(
            "And so is solving\nthe linear system!",
            target_mode="surprised",
            look_at=morty.eyes,
            added_anims=[morty.change("tease"), stds[0].change("sassy"), stds[1].change("hesitant")]
        )
        self.wait()
        self.play(stds[2].change("angry"))
        self.wait(4)

        # Hold up new screen
        new_point = 3 * UR
        self.play(
            stds[2].debubble(mode="raise_right_hand", look_at=new_point),
            stds[0].change("pondering", look_at=new_point),
            stds[1].change("pondering", look_at=new_point),
        )
        self.wait(3)
        self.play(self.change_students("erm", "hesitant", "angry"))
        self.wait(3)

        # There's a trick
        self.play(
            morty.says("But there's\na trick"),
            self.change_students("tease", "happy", "hesitant")
        )
        self.wait(2)

        fft = Text("FFT")
        fft.next_to(stds[0].get_corner(UR), UP)
        self.play(
            stds[0].change("raise_right_hand"), FadeIn(fft, UP),
            morty.change("tease", fft),
            *(pi.animate.look_at(fft) for pi in self.students[1:]),
        )
        self.wait()
        self.student_says(
            "What...is that?",
            target_mode="dance_3",
            index=1,
        )
        self.play(morty.change("happy"))
        self.wait(2)
        self.play(stds[0].change("tease"))
        self.play(stds[1].change("maybe", stds[0].eyes))
        self.wait(2)
        self.play(morty.change("well"))
        self.wait(3)
