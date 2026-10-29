# ==============================================================================
# Scene:      Narrative
# Source:     videos/_2021/some1_winners.py (lines 728-762)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Narrative.py Narrative -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Narrative(Scene):
    def construct(self):
        question = Text("What makes a good piece of exposition?", font_size=60)
        question.to_edge(UP)
        question.add(Underline(question))
        self.add(question)
        properties = VGroup(
            Text("Clarity"),
            Text("Motivation"),
            Text("Memorability"),
            Text("Narrative"),
        )
        properties.scale(60 / 48)
        properties.arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        properties.next_to(question, DOWN, LARGE_BUFF)
        properties.set_fill(BLUE)
        narrative = properties[-1]

        for prop in properties:
            dot = Dot()
            dot.next_to(prop, LEFT)
            self.play(
                FadeIn(dot, scale=0.5),
                FadeIn(prop, lag_ratio=0.1)
            )

        rect = FullScreenFadeRectangle()
        rect.set_opacity(0.5)
        self.add(rect, narrative)
        self.play(
            FadeIn(rect),
            FlashAround(narrative, run_time=2, time_width=1),
            narrative.animate.set_color(YELLOW),
        )
        self.wait()
