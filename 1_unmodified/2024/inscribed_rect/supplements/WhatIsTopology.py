# ==============================================================================
# Scene:      WhatIsTopology
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 92-167)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatIsTopology.py WhatIsTopology -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhatIsTopology(InteractiveScene):
    def construct(self):
        # Ask question
        question = Text("What is Topology?", font_size=72)
        question.to_edge(UP)
        underline = Underline(question, buff=-0.05)

        morty = Mortimer(height=3).flip()
        morty.move_to(DL)
        conf_morty = morty.copy().change_mode("confused")
        for pi in [morty, conf_morty]:
            for eye in pi.eyes:
                eye.scale(1.2, about_edge=DOWN)
        conf_morty.look_at(question)

        self.add(question)
        self.add(morty)
        self.play(
            Transform(morty, conf_morty),
            ShowCreation(underline)
        )
        self.play(Blink(morty))
        self.wait(2)

        # Answer 1
        answer1 = Text("Is it a study of bizarre shapes?", font_size=60)
        answer1.set_color(BLUE)
        answer1.next_to(question, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(answer1, lag_ratio=0.1, run_time=2),
            FadeOut(morty, DOWN)
        )
        self.wait()

        # Answer 2
        answer2 = TexText("Is it ``rubber sheet'' geometry?", font_size=60)
        answer2.set_color(BLUE)
        answer2.next_to(question, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(answer2, lag_ratio=0.1, run_time=2),
            answer1.animate.set_opacity(0.25).to_edge(DOWN)
        )
        self.wait()

        # Cross out both
        self.play(answer1.animate.set_opacity(1).next_to(answer2, DOWN, buff=MED_LARGE_BUFF), run_time=2)

        answers = VGroup(answer1, answer2)
        crosses = VGroup(Cross(a) for a in answers)
        crosses.set_stroke(RED, (0, 5, 5, 5, 0))

        self.play(ShowCreation(crosses, lag_ratio=0.25))
        self.wait()

        # How is this math?
        morty = Mortimer(height=2).flip()
        morty.to_corner(DL, buff=LARGE_BUFF)
        conf_morty = morty.copy().change_mode("maybe")
        for pi in [morty, conf_morty]:
            for eye in pi.eyes:
                eye.scale(1.2, about_edge=DOWN)
        bubble = morty.get_bubble("How is\nthis math?", SpeechBubble)

        self.play(
            FadeOut(answers),
            FadeOut(crosses),
            FadeIn(morty)
        )
        self.play(
            Transform(morty, conf_morty),
            Write(bubble),
        )
        self.play(Blink(morty))
        self.wait()
