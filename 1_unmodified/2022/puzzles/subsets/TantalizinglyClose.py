# ==============================================================================
# Scene:      TantalizinglyClose
# Source:     videos/_2022/puzzles/subsets.py (lines 4974-4996)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TantalizinglyClose.py TantalizinglyClose -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TantalizinglyClose(InteractiveScene):
    def construct(self):
        brace = Brace(Line(ORIGIN, 4.5 * RIGHT), DOWN)
        brace.to_edge(RIGHT, buff=LARGE_BUFF)
        brace.set_y(-2)
        words = brace.get_text("Tantalizingly close to\nwhat we want", font_size=36)
        randy = Randolph(height=1.5)
        randy.next_to(brace, DL)
        randy.shift(0.5 * RIGHT)

        self.play(
            GrowFromCenter(brace),
            FadeIn(randy),
        )
        self.play(
            randy.change("hooray"),
            Write(words),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, VGroup(brace, words, randy), shift=DOWN)
        )
