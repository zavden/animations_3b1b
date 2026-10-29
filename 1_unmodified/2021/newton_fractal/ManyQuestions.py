# ==============================================================================
# Scene:      ManyQuestions
# Source:     videos/_2021/newton_fractal.py (lines 3200-3229)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyQuestions.py ManyQuestions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ManyQuestions(Scene):
    def construct(self):
        self.add(FullScreenRectangle())

        questions = VGroup(
            Text("Lower order polynomials?"),
            Text("Do points ever cycle?"),
            Text("Fractal dimension?"),
            Text("Connection to Mandelbrot?"),
        )
        screens = VGroup(*(ScreenRectangle() for q in questions))
        screens.arrange_in_grid(
            v_buff=1.5,
            h_buff=3.0,
        )
        screens.set_fill(BLACK, 1)

        questions.match_width(screens[0])
        for question, screen in zip(questions, screens):
            question.next_to(screen, UP)
            screen.add(question)

        screens.set_height(FRAME_HEIGHT - 0.5)
        screens.center()

        self.play(LaggedStartMap(
            FadeIn, screens,
            lag_ratio=0.9,
        ), run_time=8)
        self.wait()
