# ==============================================================================
# Scene:      LocationTracking
# Source:     videos/_2020/ctracing.py (lines 432-488)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LocationTracking.py LocationTracking -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LocationTracking(Scene):
    def construct(self):
        question = OldTexText(
            "Would you like this company to track\\\\",
            "and occasionally sell your location?"
        )
        question.to_edge(UP, buff=LARGE_BUFF)

        slider = Rectangle(width=1.25, height=0.5)
        slider.round_corners(radius=0.25)
        slider.set_fill(GREEN, 1)
        slider.next_to(question, DOWN, buff=MED_LARGE_BUFF)

        dot = Dot(radius=0.25)
        dot.set_fill(GREY_C, 1)
        dot.set_stroke(WHITE, 3)
        dot.move_to(slider, RIGHT)

        morty = Mortimer()
        morty.next_to(slider, RIGHT)
        morty.to_edge(DOWN)

        bubble = morty.get_bubble(
            height=2,
            width=3,
            direction=LEFT,
        )

        answer = OldTexText("Um...", "no.")
        answer.set_height(0.4)
        answer.set_color(YELLOW)
        bubble.add_content(answer)

        self.add(morty)

        self.play(
            FadeInFromDown(question),
            Write(slider),
            FadeIn(dot),
        )
        self.play(morty.change, "confused", slider)
        self.play(Blink(morty))
        self.play(
            FadeIn(bubble),
            Write(answer[0]),
        )
        self.wait()
        self.play(
            dot.move_to, slider, LEFT,
            slider.set_fill, {"opacity": 0},
            FadeIn(answer[1]),
            morty.change, "sassy"
        )
        self.play(Blink(morty))
        self.wait(2)
        self.play(Blink(morty))
        self.wait(2)
