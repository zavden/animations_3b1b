# ==============================================================================
# Scene:      SimpleQuestion
# Source:     videos/_2023/convolutions2/supplements.py (lines 663-704)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleQuestion.py SimpleQuestion -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SimpleQuestion(InteractiveScene):
    def construct(self):
        # Rectangles
        rects = ScreenRectangle().replicate(2)
        rects.set_height(0.45 * FRAME_HEIGHT)
        rects.arrange(RIGHT, buff=0.75).shift(0.5 * DOWN)

        # Equations
        equations = VGroup(
            Tex("X + Y", font_size=60),
            Tex(R"\int_{-\infty}^\infty f(x)g(s - x)dx"),
        )
        for equation, rect in zip(equations, rects):
            equation.next_to(rect, UP)

        # Words
        words = VGroup(
            Text("Such a \n simple question!"),
            Text(
                "Such a seemingly \n simple question.",
                t2s={"seemingly": ITALIC},
                t2c={"seemingly": YELLOW},
            )
        )
        for word in words:
            word.match_x(rects[0])
            word.to_edge(UP, buff=MED_SMALL_BUFF)

        self.play(
            Write(words[0], run_time=1),
            FadeIn(equations[0])
        )
        self.wait()
        self.play(TransformMatchingStrings(
            words[0], words[1],
            key_map={"!": "."},
            run_time=1,
        ))
        self.wait()
        # self.play(Write(equations[1]))
        self.play(TransformFromCopy(equations[0], equations[1]), run_time=2, lag_ratio=0.02)
        self.wait(2)
