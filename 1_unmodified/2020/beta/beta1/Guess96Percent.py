# ==============================================================================
# Scene:      Guess96Percent
# Source:     videos/_2020/beta/beta1.py (lines 3369-3395)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Guess96Percent.py Guess96Percent -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Guess96Percent(Scene):
    def construct(self):
        randy = Randolph()
        randy.set_height(1)

        bubble = SpeechBubble(height=2, width=3)
        bubble.pin_to(randy)
        words = OldTexText("96$\\%$, right?")
        fix_percent(words[0][2])
        bubble.add_content(words)

        arrow = Vector(2 * RIGHT + DOWN)
        arrow.next_to(randy, RIGHT)
        arrow.shift(2 * UP)

        self.play(
            FadeIn(randy),
            ShowCreation(bubble),
            Write(words),
        )
        self.play(randy.change, "shruggie", randy.get_right() + RIGHT)
        self.play(ShowCreation(arrow))
        for x in range(2):
            self.play(Blink(randy))
            self.wait()

        self.embed()
