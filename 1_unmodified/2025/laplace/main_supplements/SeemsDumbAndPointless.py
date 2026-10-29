# ==============================================================================
# Scene:      SeemsDumbAndPointless
# Source:     videos/_2025/laplace/main_supplements.py (lines 558-593)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SeemsDumbAndPointless.py SeemsDumbAndPointless -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SeemsDumbAndPointless(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        self.play(LaggedStart(
            stds[0].says("Seems dumb", mode="sassy", look_at=self.screen),
            Animation(Point()),
            stds[2].animate.look_at(self.screen),
            morty.change('guilty'),
            stds[1].says(
                "And pointless!",
                mode="maybe",
                look_at=self.screen,
                bubble_direction=LEFT,
                bubble_creation_class=FadeIn
            ),
            # stds[1].animate.look_at(self.screen),
            lag_ratio=0.25
        ))
        self.wait(7)

        # Show Analytic Continuation
        words = Text("Analytic\nContinuation", font_size=60)
        words.next_to(morty, UP, LARGE_BUFF)
        words.match_x(morty.get_left())

        self.wait(2)
        self.play(
            stds[0].debubble("pondering", look_at=words),
            stds[1].debubble("pondering", look_at=words),
            stds[2].change("pondering", words),
            morty.change("raise_right_hand"),
            Write(words),
        )
        self.wait(7)
