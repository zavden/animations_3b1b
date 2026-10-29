# ==============================================================================
# Scene:      Timeline
# Source:     videos/_2024/antp/main.py (lines 85-131)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Timeline.py Timeline -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Timeline(InteractiveScene):
    def construct(self):
        # Timeline
        timeline = NumberLine(
            (-500, 2050, 100),
            width=FRAME_WIDTH - 1
        )
        timeline.move_to(2.5 * DOWN)
        timeline.add_numbers(
            list(range(0, 2050, 500)),
            direction=DOWN,
            group_with_commas=False,
            font_size=36,
        )
        label = Tex(R"\sim 300 BC", font_size=36)
        v_line = Line(DOWN, UP)
        v_line.move_to(timeline.n2p(-300), DOWN)
        v_line.shift(SMALL_BUFF * DOWN)
        v_line.set_stroke(WHITE, 1)
        label.next_to(v_line, DOWN, buff=0.15)

        self.add(timeline)
        self.add(v_line)
        self.add(label)

        # Label
        question = TexText(
            R"``Are there infinitely many twin primes?''\\ \quad -Euclid",
            font_size=48,
            alignment="",
        )
        question[-7:].shift(RIGHT + 0.1 * DOWN)
        question.next_to(v_line, UP)
        question.shift_onto_screen(buff=0.2)

        arrows = VGroup(
            Vector(3 * LEFT),
            Text("No one can\nanswer", font_size=60).set_color(YELLOW),
            Vector(3 * RIGHT)
        )
        arrows.arrange(RIGHT)
        arrows.set_width(get_norm(timeline.n2p(2000) - timeline.n2p(-300)))
        arrows.next_to(v_line, RIGHT)
        arrows.shift(0.5 * UP)

        # self.add(question)
        self.add(arrows)
