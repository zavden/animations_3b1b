# ==============================================================================
# Scene:      NextVideoInlay
# Source:     videos/_2023/clt/wordy_scenes.py (lines 319-384)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/clt/main.py
#
# Run from this folder:
#     manimgl NextVideoInlay.py NextVideoInlay -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2023/clt/main.py -----

def gauss_func(x, mu, sigma):
    pre_factor = 1 / (sigma * math.sqrt(2 * PI))
    return pre_factor * np.exp(-0.5 * ((x - mu) / sigma)**2)



# ----- From _2023/clt/wordy_scenes.py -----

class NextVideoInlay(InteractiveScene):
    def construct(self):
        # Graph
        plane = NumberPlane(
            (-5, 5), (-0.25, 1.0, 0.25),
            width=2.5, height=1.25,
            background_line_style=dict(
                stroke_color=GREY_B,
                stroke_width=1,
            ),
            faded_line_style=dict(
                stroke_color=GREY_B,
                stroke_width=1,
                stroke_opacity=0.25,
            ),
            faded_line_ratio=4
        )
        plane.set_height(FRAME_HEIGHT)

        graph = plane.get_graph(lambda x: gauss_func(x, 0, 1))
        graph.set_stroke(YELLOW, 3)

        self.add(plane)
        self.play(
            VShowPassingFlash(graph.copy().set_stroke(TEAL, 10), time_width=1.5),
            ShowCreation(graph),
            run_time=2
        )

        # Function name
        expr = Tex(
            R"{1 \over \sqrt{2\pi}} e^{-x^2 / 2}",
        )
        expr.set_height(3)
        expr.next_to(plane.c2p(0, 0.25), UP)
        expr.to_edge(LEFT)
        expr.set_backstroke(width=20)

        self.play(Write(expr, lag_ratio=0.1))
        self.wait()

        # Questions
        rects = VGroup(
            SurroundingRectangle(expr["e^{-x^2 / 2}"]).set_stroke(TEAL, 5),
            SurroundingRectangle(expr[R"\pi"]).set_stroke(RED, 5),
        )
        questions = [
            Text("Why this function?"),
            Text("Where's\nthe circle?", alignment="LEFT"),
        ]
        for question, rect, vect in zip(questions, rects, [UP, DOWN]):
            question.scale(2)
            question.next_to(rect, vect, MED_LARGE_BUFF, aligned_edge=LEFT)
            question.match_color(rect)
            question.set_backstroke(width=20)

        self.play(
            FadeIn(questions[0]),
            ShowCreation(rects[0]),
        )
        self.wait()
        self.play(
            FadeIn(questions[1]),
            ShowCreation(rects[1]),
        )
        self.wait()
