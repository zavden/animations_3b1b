# ==============================================================================
# Scene:      ForgetTheBestWord
# Source:     videos/_2022/wordle/footnote.py (lines 818-843)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ForgetTheBestWord.py ForgetTheBestWord -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ForgetTheBestWord(Scene):
    def construct(self):
        self.add(FullScreenRectangle())

        randy = Randolph()
        randy.to_corner(DL)
        text = OldTexText("Wait, was it ``slane'',\\\\``salet'' or ``soare''?")

        self.play(PiCreatureBubbleIntroduction(
            randy, text,
            bubble_type=ThoughtBubble,
            target_mode="confused",
        ))
        self.play(Blink(randy))
        self.wait()

        randy.bubble.add(text)
        self.play(
            FadeOut(randy.bubble, scale=0.25, shift=2 * DL),
            randy.change("erm")
        )
        self.wait()
        self.play(randy.change("thinking", UR))
        for x in range(2):
            self.play(Blink(randy))
            self.wait(2)
